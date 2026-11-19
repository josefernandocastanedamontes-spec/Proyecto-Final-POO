# -*- coding: utf-8 -*-
from typing import Dict, List, Optional
from controlador.controlador_ronda import ControladorRonda
from controlador.controlador_votacion import ControladorVotacion
from modelos.categoria import Categoria
from modelos.configuracionpartida import ConfiguracionPartida
from modelos.enumeraciones import EstadoJugador
from modelos.jugador import Jugador
from modelos.partida import Partida
from modelos.resultadopartida import ResultadoPartida
from servicios.asignacion import IAsignadorRoles
from servicios.conteo import IContadorVotos
from servicios.palabras import IRepositorioPalabras
from servicios.validacion import ValidadorLongitud, ValidadorPalabraProhibida, ValidadorPistaCompuesto
from vista.interfaces import IVistaJuego


class ControladorPartida:
    """Controlador principal; recibe sus dependencias mediante inyeccion."""

    def __init__(self, vista: IVistaJuego, repositorio_palabras: IRepositorioPalabras,
                 asignador_roles: IAsignadorRoles, contador_votos: IContadorVotos):
        self._vista = vista
        self._repositorio_palabras = repositorio_palabras
        self._asignador_roles = asignador_roles
        self._contador_votos = contador_votos
        self._nombres_registrados: List[str] = []
        self._marcador_acumulado: Dict[str, int] = {}
        self._ultima_config: Optional[ConfiguracionPartida] = None
        self._partida_actual: Optional[Partida] = None
        self._jugadores_ordenados: List[Jugador] = []
        self._resumen_rondas: List[str] = []

    def iniciar_aplicacion(self) -> None:
        self._abrir_pantalla_registro()
        self._vista.iniciar()

    def _abrir_pantalla_registro(self) -> None:
        self._vista.mostrar_registro(
            categorias=self._repositorio_palabras.obtener_categorias_disponibles(),
            jugadores_actuales=list(self._nombres_registrados),
            on_agregar_jugador=self._agregar_jugador,
            on_eliminar_jugador=self._eliminar_jugador,
            on_iniciar_partida=self._configurar_e_iniciar_partida,
        )

    def _agregar_jugador(self, nombre: str) -> None:
        limpio = nombre.strip()
        if not limpio:
            self._vista.mostrar_error("Nombre vacio", "Ingresa un nombre valido.")
            return
        if len(self._nombres_registrados) >= 10:
            self._vista.mostrar_error("Limite alcanzado", "El maximo permitido es de 10 jugadores.")
            return
        if any(n.casefold() == limpio.casefold() for n in self._nombres_registrados):
            self._vista.mostrar_error("Nombre duplicado", f"El jugador '{limpio}' ya esta registrado.")
            return
        self._nombres_registrados.append(limpio)
        self._marcador_acumulado.setdefault(limpio, 0)
        self._abrir_pantalla_registro()

    def _eliminar_jugador(self, indice: int) -> None:
        if 0 <= indice < len(self._nombres_registrados):
            eliminado = self._nombres_registrados.pop(indice)
            self._marcador_acumulado.pop(eliminado, None)
            self._abrir_pantalla_registro()

    def _configurar_e_iniciar_partida(self, nombre_categoria: str, numero_rondas: int,
                                      tiempo_debate: int, longitud_max_pista: int,
                                      ultima_oportunidad: bool) -> None:
        if not 3 <= len(self._nombres_registrados) <= 10:
            self._vista.mostrar_error("Jugadores insuficientes", "Debes registrar entre 3 y 10 jugadores para iniciar.")
            return
        try:
            config = ConfiguracionPartida(
                numero_rondas=int(numero_rondas),
                tiempo_debate=int(tiempo_debate),
                categoria=Categoria(nombre_categoria),
                ultima_oportunidad=bool(ultima_oportunidad),
                longitud_max_pista=int(longitud_max_pista),
            )
            config.validar()
            self._ultima_config = config
            self._comenzar_partida(config)
        except (ValueError, TypeError) as exc:
            self._vista.mostrar_error("Configuracion invalida", str(exc))

    def _comenzar_partida(self, config: ConfiguracionPartida) -> None:
        jugadores = [Jugador(i + 1, nombre) for i, nombre in enumerate(self._nombres_registrados)]
        self._jugadores_ordenados = list(jugadores)
        self._marcador_acumulado = {j.nombre: 0 for j in jugadores}
        self._resumen_rondas = []
        self._partida_actual = Partida(jugadores, config)
        self._partida_actual.iniciar()
        validador = ValidadorPistaCompuesto([
            ValidadorLongitud(config.longitud_max_pista),
            ValidadorPalabraProhibida(),
        ])
        self._ctrl_ronda = ControladorRonda(self._vista, validador)
        self._ctrl_votacion = ControladorVotacion(self._vista, self._contador_votos)
        self._ejecutar_siguiente_ronda()

    def _ejecutar_siguiente_ronda(self) -> None:
        partida = self._partida_actual
        config = self._ultima_config
        if len(partida.rondas) >= config.numero_rondas:
            self._finalizar_partida()
            return

        # Cada ronda empieza con participantes activos, palabra nueva y roles nuevos.
        for jugador in self._jugadores_ordenados:
            jugador.estado = EstadoJugador.ACTIVO
        palabra = self._repositorio_palabras.obtener_palabra_aleatoria(config.categoria)
        partida.palabra_secreta = palabra
        self._asignador_roles.asignar_roles(partida.jugadores, palabra)
        self._ctrl_ronda.iniciar_asignacion_roles(
            jugadores=self._jugadores_ordenados,
            al_finalizar=self._iniciar_flujo_ronda,
        )

    def _iniciar_flujo_ronda(self) -> None:
        partida = self._partida_actual
        config = self._ultima_config
        ronda = partida.nueva_ronda()
        self._ctrl_ronda.iniciar_fase_pistas(
            partida=partida,
            ronda=ronda,
            jugadores_ordenados=self._jugadores_ordenados,
            longitud_maxima=config.longitud_max_pista,
            al_finalizar_pistas=lambda: self._ctrl_ronda.iniciar_fase_debate(
                partida=partida,
                ronda=ronda,
                segundos_debate=config.tiempo_debate,
                al_finalizar_debate=lambda: self._ctrl_votacion.iniciar_votacion(
                    ronda=ronda,
                    jugadores_ordenados=self._jugadores_ordenados,
                    al_finalizar_votacion=lambda acusado: self._evaluar_votacion(ronda, acusado),
                ),
            ),
        )

    def _evaluar_votacion(self, ronda, acusado: Optional[Jugador]) -> None:
        partida = self._partida_actual
        config = self._ultima_config

        # Regla provisional: si el segundo desempate persiste, el impostor gana
        # la ronda por supervivencia. Debe confirmarse con el docente.
        if acusado is None:
            self._cerrar_ronda(
                ronda, "Impostor", "El desempate termino igualado; el impostor sobrevive.", None
            )
            return

        if not acusado.rol.conoce_palabra():
            if config.ultima_oportunidad:
                def verificar_adivinanza(intento: str) -> None:
                    acerto = acusado.rol.intentar_adivinar(intento) and partida.palabra_secreta.coincide_con(intento)
                    if acerto:
                        self._cerrar_ronda(
                            ronda, "Impostor",
                            f"{acusado.nombre} fue descubierto, pero adivino la palabra secreta.", acusado,
                        )
                    else:
                        self._cerrar_ronda(
                            ronda, "Civiles",
                            f"Descubrieron a {acusado.nombre} y fallo su ultimo intento.", acusado,
                        )
                self._vista.solicitar_ultima_oportunidad(
                    nombre_impostor=acusado.nombre,
                    on_adivinar_palabra=verificar_adivinanza,
                )
            else:
                self._cerrar_ronda(
                    ronda, "Civiles", f"Atraparon al impostor ({acusado.nombre}).", acusado
                )
            return

        acusado.estado = EstadoJugador.ELIMINADO
        self._cerrar_ronda(
            ronda, "Impostor",
            f"El grupo senalo a {acusado.nombre}, quien era civil; el impostor gana la ronda.",
            acusado,
        )

    def _cerrar_ronda(self, ronda, ganador: str, detalle: str,
                      acusado: Optional[Jugador]) -> None:
        partida = self._partida_actual
        roles_dict = {j.nombre: j.rol.nombre for j in self._jugadores_ordenados}
        resultado = ResultadoPartida(ganador, acusado, roles_dict)
        partida.registrar_resultado(resultado)

        if ganador == "Civiles":
            for jugador in self._jugadores_ordenados:
                if jugador.rol.conoce_palabra():
                    self._marcador_acumulado[jugador.nombre] += 1
        else:
            impostor = next(j for j in self._jugadores_ordenados if not j.rol.conoce_palabra())
            self._marcador_acumulado[impostor.nombre] += 1

        self._resumen_rondas.append(f"Ronda {ronda.numero}: {ganador}. {detalle}")
        if len(partida.rondas) < self._ultima_config.numero_rondas:
            self._vista.mostrar_info(
                f"Fin de la ronda {ronda.numero}",
                f"{detalle}\nMarcador actualizado. Se preparara una nueva palabra y una nueva asignacion de roles.",
            )
            self._ejecutar_siguiente_ronda()
        else:
            self._finalizar_partida()

    def _finalizar_partida(self) -> None:
        partida = self._partida_actual
        if not partida.rondas:
            return
        puntaje_maximo = max(self._marcador_acumulado.values(), default=0)
        ganadores = [n for n, puntos in self._marcador_acumulado.items() if puntos == puntaje_maximo]
        ganador_texto = "Empate en el marcador" if len(ganadores) > 1 else f"Ganador por puntos: {ganadores[0]}"
        detalle = "\n".join(self._resumen_rondas)
        ultimo_resultado = partida.determinar_ganador()
        palabra = partida.palabra_secreta.texto if partida.palabra_secreta else "No disponible"
        if ultimo_resultado:
            detalle += f"\n\nUltimo resultado: {ultimo_resultado.generar_resumen()}"
        roles_tabla = [
            (j.nombre, j.rol.nombre, "Activo" if j.estado == EstadoJugador.ACTIVO else "Eliminado")
            for j in self._jugadores_ordenados
        ]
        self._vista.mostrar_resultado_final(
            ganador=ganador_texto,
            detalle=detalle,
            palabra_secreta=palabra,
            roles_revelados=roles_tabla,
            marcador_acumulado=dict(self._marcador_acumulado),
            on_nueva_partida=lambda: self._comenzar_partida(self._ultima_config),
            on_volver_registro=self._abrir_pantalla_registro,
        )
