# -*- coding: utf-8 -*-
from typing import Dict, List, Optional
from controlador.controlador_ronda import ControladorRonda
from controlador.controlador_votacion import ControladorVotacion
from modelos.categoria import Categoria
from modelos.configuracionpartida import ConfiguracionPartida
from modelos.enumeraciones import EstadoJugador, FaseJuego
from modelos.jugador import Jugador
from modelos.partida import Partida
from modelos.resultadopartida import ResultadoPartida
from servicios.asignacion import IAsignadorRoles
from servicios.conteo import IContadorVotos
from servicios.palabras import RepositorioPalabrasMemoria
from servicios.validacion import (
    ValidadorLongitud,
    ValidadorPalabraProhibida,
    ValidadorPistaCompuesto,
)
from vista.interfaces import IVistaJuego


class ControladorPartida:
    """Controlador principal (Inyección de Dependencias - Principio D de SOLID)."""

    def __init__(
        self,
        vista: IVistaJuego,
        repositorio_palabras: RepositorioPalabrasMemoria,
        asignador_roles: IAsignadorRoles,
        contador_votos: IContadorVotos,
    ):
        self._vista = vista
        self._repositorio_palabras = repositorio_palabras
        self._asignador_roles = asignador_roles
        self._contador_votos = contador_votos

        self._nombres_registrados: List[str] = []
        self._marcador_acumulado: Dict[str, int] = {}
        self._ultima_config: Optional[ConfiguracionPartida] = None
        self._partida_actual: Optional[Partida] = None
        self._jugadores_ordenados: List[Jugador] = []

    def iniciar_aplicacion(self) -> None:
        self._abrir_pantalla_registro()
        self._vista.iniciar()

    def _abrir_pantalla_registro(self) -> None:
        categorias = self._repositorio_palabras.obtener_categorias_disponibles()
        self._vista.mostrar_registro(
            categorias=categorias,
            jugadores_actuales=list(self._nombres_registrados),
            on_agregar_jugador=self._agregar_jugador,
            on_eliminar_jugador=self._eliminar_jugador,
            on_iniciar_partida=self._configurar_e_iniciar_partida,
        )

    def _agregar_jugador(self, nombre: str) -> None:
        limpio = nombre.strip()
        if not limpio:
            self._vista.mostrar_error("Nombre vacío", "Ingresa un nombre válido.")
            return
        if len(self._nombres_registrados) >= 10:
            self._vista.mostrar_error(
                "Límite alcanzado", "El máximo permitido es de 10 jugadores."
            )
            return
        if any(n.lower() == limpio.lower() for n in self._nombres_registrados):
            self._vista.mostrar_error(
                "Nombre duplicado", f"El jugador '{limpio}' ya está registrado."
            )
            return

        self._nombres_registrados.append(limpio)
        self._marcador_acumulado.setdefault(limpio, 0)
        self._abrir_pantalla_registro()

    def _eliminar_jugador(self, indice: int) -> None:
        if 0 <= indice < len(self._nombres_registrados):
            eliminado = self._nombres_registrados.pop(indice)
            self._marcador_acumulado.pop(eliminado, None)
            self._abrir_pantalla_registro()

    def _configurar_e_iniciar_partida(
        self,
        nombre_categoria: str,
        numero_rondas: int,
        tiempo_debate: int,
        longitud_max_pista: int,
        ultima_oportunidad: bool,
    ) -> None:
        if len(self._nombres_registrados) < 3:
            self._vista.mostrar_error(
                "Jugadores insuficientes",
                "Debes registrar entre 3 y 10 jugadores para iniciar.",
            )
            return

        try:
            categoria = Categoria(nombre_categoria)
            config = ConfiguracionPartida(
                numero_rondas=int(numero_rondas),
                tiempo_debate=int(tiempo_debate),
                categoria=categoria,
                ultima_oportunidad=bool(ultima_oportunidad),
                longitud_max_pista=int(longitud_max_pista),
            )
            config.validar()
            self._ultima_config = config
            self._comenzar_partida(config)
        except ValueError as exc:
            self._vista.mostrar_error("Configuración inválida", str(exc))

    def _comenzar_partida(self, config: ConfiguracionPartida) -> None:
        jugadores = [
            Jugador(id_jugador=i + 1, nombre=nombre)
            for i, nombre in enumerate(self._nombres_registrados)
        ]
        self._jugadores_ordenados = list(jugadores)

        partida = Partida(jugadores=jugadores, configuracion=config)
        partida.iniciar()

        palabra = self._repositorio_palabras.obtener_palabra_aleatoria(
            config._categoria
        )
        partida.palabra_secreta = palabra
        self._asignador_roles.asignar_roles(partida.jugadores, palabra)

        self._partida_actual = partida
        validador = ValidadorPistaCompuesto(
            [
                ValidadorLongitud(config._longitud_max_pista),
                ValidadorPalabraProhibida(),
            ]
        )
        self._ctrl_ronda = ControladorRonda(self._vista, validador)
        self._ctrl_votacion = ControladorVotacion(self._vista, self._contador_votos)

        self._ctrl_ronda.iniciar_asignacion_roles(
            jugadores=self._jugadores_ordenados,
            al_finalizar=self._ejecutar_siguiente_ronda,
        )

    def _ejecutar_siguiente_ronda(self) -> None:
        partida = self._partida_actual
        config = self._ultima_config
        ronda = partida.nueva_ronda()

        self._ctrl_ronda.iniciar_fase_pistas(
            partida=partida,
            ronda=ronda,
            jugadores_ordenados=self._jugadores_ordenados,
            longitud_maxima=config._longitud_max_pista,
            al_finalizar_pistas=lambda: self._ctrl_ronda.iniciar_fase_debate(
                partida=partida,
                ronda=ronda,
                segundos_debate=config._tiempo_debate,
                al_finalizar_debate=lambda: self._ctrl_votacion.iniciar_votacion(
                    ronda=ronda,
                    jugadores_ordenados=self._jugadores_ordenados,
                    al_finalizar_votacion=lambda acusado: self._evaluar_votacion(
                        ronda, acusado
                    ),
                ),
            ),
        )

    def _evaluar_votacion(self, ronda, acusado: Optional[Jugador]) -> None:
        partida = self._partida_actual
        config = self._ultima_config

        # Caso 1: Empate en la votación
        if acusado is None:
            if ronda.numero < config._numero_rondas:
                self._vista.mostrar_info(
                    "Empate en la votación",
                    "Hubo empate de votos. Nadie fue eliminado; inicia una nueva ronda.",
                )
                self._ejecutar_siguiente_ronda()
            else:
                self._finalizar_partida(
                    ganador="¡Gana el Impostor!",
                    detalle="Se agotaron las rondas tras un empate sin descubrir al impostor.",
                    acusado=None,
                    civiles_ganan=False,
                )
            return

        # Caso 2: El más votado es el Impostor (Polimorfismo: no conoce la palabra)
        if not acusado.rol.conoce_palabra():
            if config._ultima_oportunidad:
                def verificar_adivinanza(intento: str) -> None:
                    if acusado.rol.intentar_adivinar(
                        intento
                    ) and partida.palabra_secreta.coincide_con(intento):
                        self._finalizar_partida(
                            ganador="¡Gana el Impostor!",
                            detalle=f"{acusado.nombre} fue descubierto, pero adivinó la palabra secreta.",
                            acusado=acusado,
                            civiles_ganan=False,
                        )
                    else:
                        self._finalizar_partida(
                            ganador="¡Ganan los Civiles!",
                            detalle=f"Descubrieron a {acusado.nombre} y falló su último intento.",
                            acusado=acusado,
                            civiles_ganan=True,
                        )

                self._vista.solicitar_ultima_oportunidad(
                    nombre_impostor=acusado.nombre,
                    on_adivinar_palabra=verificar_adivinanza,
                )
            else:
                self._finalizar_partida(
                    ganador="¡Ganan los Civiles!",
                    detalle=f"¡Atraparon al impostor ({acusado.nombre})!",
                    acusado=acusado,
                    civiles_ganan=True,
                )
            return

        # Caso 3: Acusaron a un Civil inocente (RF-10)
        acusado.estado = EstadoJugador.ELIMINADO
        activos = [
            j for j in self._jugadores_ordenados if j.estado == EstadoJugador.ACTIVO
        ]

        if len(activos) <= 2 or ronda.numero >= config._numero_rondas:
            self._finalizar_partida(
                ganador="¡Gana el Impostor!",
                detalle=f"Eliminaron al inocente {acusado.nombre}. El impostor logró sobrevivir.",
                acusado=acusado,
                civiles_ganan=False,
            )
        else:
            self._vista.mostrar_info(
                "Inocente Eliminado",
                f"{acusado.nombre} era CIVIL y queda eliminado.\nEl impostor sigue oculto. ¡Comienza la siguiente ronda!",
            )
            self._ejecutar_siguiente_ronda()

    def _finalizar_partida(
        self,
        ganador: str,
        detalle: str,
        acusado: Optional[Jugador],
        civiles_ganan: bool,
    ) -> None:
        partida = self._partida_actual
        if partida.rondas:
            partida.rondas[-1]._fase = FaseJuego.RESULTADO

        roles_dict = {j.nombre: j.rol.nombre for j in self._jugadores_ordenados}
        resultado = ResultadoPartida(
            ganador=ganador, acusado=acusado, roles_revelados=roles_dict
        )

        # Actualizar marcador acumulado (RF-11)
        for j in self._jugadores_ordenados:
            es_civil = j.rol.conoce_palabra()
            if (civiles_ganan and es_civil) or (not civiles_ganan and not es_civil):
                self._marcador_acumulado[j.nombre] = (
                    self._marcador_acumulado.get(j.nombre, 0) + 1
                )

        roles_tabla = [
            (
                j.nombre,
                j.rol.nombre,
                "Activo" if j.estado == EstadoJugador.ACTIVO else "Eliminado",
            )
            for j in self._jugadores_ordenados
        ]

        self._vista.mostrar_resultado_final(
            ganador=ganador,
            detalle=f"{detalle} ({resultado.generar_resumen()})",
            palabra_secreta=partida.palabra_secreta.texto,
            roles_revelados=roles_tabla,
            marcador_acumulado=dict(self._marcador_acumulado),
            on_nueva_partida=lambda: self._comenzar_partida(self._ultima_config),
            on_volver_registro=self._abrir_pantalla_registro,
        )
