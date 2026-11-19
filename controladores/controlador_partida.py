from modelos.categoria import Categoria
from modelos.configuracionpartida import ConfiguracionPartida
from modelos.jugador import Jugador
from modelos.partida import Partida
from modelos.enumeraciones import FaseJuego
from modelos.excepciones import FaseInvalidaException
from servicios.asignacion import AsignadorRolesAleatorio
from servicios.palabras import RepositorioPalabrasMemoria
from servicios.conteo import ContadorVotosMayoria
from servicios.validacion import (
    ValidadorPistaCompuesto,
    ValidadorPalabraProhibida,
    ValidadorLongitud,
)


class ControladorPartida:
    """Coordina los casos de uso sin depender de una interfaz concreta."""

    def __init__(self, asignador=None, repositorio=None, contador=None, validador=None):
        self._asignador = asignador or AsignadorRolesAleatorio()
        self._repositorio = repositorio or RepositorioPalabrasMemoria()
        self._contador = contador or ContadorVotosMayoria()
        self._validador_externo = validador
        self._validador = validador
        self._partida = None
        self._indice_pista = 0
        self._votantes = set()
        self._votantes_desempate = set()

    @property
    def partida(self):
        return self._partida

    @property
    def jugadores(self):
        return self._partida.jugadores if self._partida else []

    @property
    def ronda(self):
        return self._partida.ronda_actual if self._partida else None

    def iniciar_partida(self, nombres, numero_rondas=3, tiempo_debate=60,
                        categoria="Lugares", ultima_oportunidad=True,
                        longitud_max_pista=40):
        nombres_limpios = [n.strip() for n in nombres if isinstance(n, str) and n.strip()]
        jugadores = [Jugador(i + 1, nombre) for i, nombre in enumerate(nombres_limpios)]
        configuracion = ConfiguracionPartida(
            numero_rondas, tiempo_debate, Categoria(categoria),
            ultima_oportunidad, longitud_max_pista,
        )
        self._partida = Partida(
            jugadores, configuracion, asignador=self._asignador,
            repositorio_palabras=self._repositorio, contador_votos=self._contador,
        )
        self._partida.iniciar()
        self._partida.ronda_actual.avanzar_fase(FaseJuego.REVELACION)
        self._indice_pista = 0
        self._votantes.clear()
        self._votantes_desempate.clear()
        self._validador = self._validador_externo or ValidadorPistaCompuesto([
            ValidadorPalabraProhibida(), ValidadorLongitud(longitud_max_pista),
        ])
        return self._partida

    def informacion_privada(self, jugador):
        if jugador not in self.jugadores or self.ronda.fase is not FaseJuego.REVELACION:
            raise FaseInvalidaException("No se puede revelar el rol en este momento.")
        if jugador.rol is None:
            raise FaseInvalidaException("El jugador todavía no tiene un rol asignado.")
        return jugador.rol.obtener_palabra_visible()

    def confirmar_revelacion(self):
        if self.ronda.fase is not FaseJuego.REVELACION:
            raise FaseInvalidaException("La fase de revelación ya terminó.")
        self.ronda.avanzar_fase(FaseJuego.PISTAS)
        return True

    def jugador_turno_pista(self):
        if self.ronda.fase is not FaseJuego.PISTAS:
            raise FaseInvalidaException("No estamos en la fase de pistas.")
        return self.jugadores[self._indice_pista]

    def registrar_pista(self, texto):
        jugador = self.jugador_turno_pista()
        pista = jugador.dar_pista(texto, self._indice_pista + 1)
        self._validador.validar(pista, self._partida.palabra_secreta)
        self.ronda.registrar_pista(pista)
        self._indice_pista += 1
        if self._indice_pista == len(self.jugadores):
            self.ronda.avanzar_fase(FaseJuego.DEBATE)
            return True
        return False

    def finalizar_debate(self):
        if self.ronda.fase is not FaseJuego.DEBATE:
            raise FaseInvalidaException("No estamos en la fase de debate.")
        self.ronda.avanzar_fase(FaseJuego.VOTACION)
        self._votantes.clear()
        return True

    def registrar_voto(self, votante, acusado):
        if self.ronda.fase is not FaseJuego.VOTACION:
            raise FaseInvalidaException("No estamos en la fase de votación.")
        if votante in self._votantes:
            from modelos.excepciones import VotoInvalidoException
            raise VotoInvalidoException("Este jugador ya registró su voto.")
        voto = votante.votar(acusado)
        self.ronda.registrar_voto(voto)
        self._votantes.add(votante)
        if len(self._votantes) < len(self.jugadores):
            return {"estado": "votando", "pendientes": len(self.jugadores) - len(self._votantes)}
        conteo = self._contador.contar_votos(self.ronda.votos)
        if conteo.hay_empate:
            self.ronda.iniciar_desempate(conteo.empatados)
            self._votantes_desempate.clear()
            return {"estado": "desempate", "candidatos": conteo.empatados}
        if conteo.sin_votos:
            return {"estado": "resultado", "resultado": self._partida.determinar_ganador(empate=True)}
        self.ronda.establecer_acusado(conteo.acusado)
        return self._resolver_acusacion(conteo.acusado)

    def registrar_voto_desempate(self, votante, acusado):
        if self.ronda.fase is not FaseJuego.DESEMPATE:
            raise FaseInvalidaException("No estamos en el desempate.")
        if votante in self._votantes_desempate:
            from modelos.excepciones import VotoInvalidoException
            raise VotoInvalidoException("Este jugador ya votó en el desempate.")
        voto = votante.votar(acusado)
        self.ronda.registrar_voto_desempate(voto)
        self._votantes_desempate.add(votante)
        if len(self._votantes_desempate) < len(self.jugadores):
            return {"estado": "desempate_votando", "pendientes": len(self.jugadores) - len(self._votantes_desempate)}
        conteo = self._contador.contar_votos(self.ronda.votos_desempate)
        if conteo.hay_empate or conteo.sin_votos:
            return {"estado": "resultado", "resultado": self._partida.determinar_ganador(empate=True)}
        self.ronda.establecer_acusado(conteo.acusado)
        return self._resolver_acusacion(conteo.acusado)

    def _resolver_acusacion(self, acusado):
        impostor = next(j for j in self.jugadores if j.rol.nombre == "Impostor")
        if acusado is impostor and self._partida.configuracion.ultima_oportunidad:
            return {"estado": "ultima_oportunidad", "impostor": impostor}
        resultado = self._partida.determinar_ganador(acusado=acusado)
        return {"estado": "resultado", "resultado": resultado}

    def resolver_ultima_oportunidad(self, adivinanza):
        if self.ronda.fase not in (FaseJuego.VOTACION, FaseJuego.DESEMPATE):
            raise FaseInvalidaException("No hay una última oportunidad pendiente.")
        return self._partida.determinar_ganador(
            acusado=self.ronda.acusado, adivinanza=adivinanza
        )

    def siguiente_ronda(self):
        ronda = self._partida.nueva_ronda()
        ronda.avanzar_fase(FaseJuego.REVELACION)
        self._indice_pista = 0
        self._votantes.clear()
        self._votantes_desempate.clear()
        self._validador = self._validador_externo or ValidadorPistaCompuesto([
            ValidadorPalabraProhibida(),
            ValidadorLongitud(self._partida.configuracion.longitud_max_pista),
        ])
        return ronda

    def hay_mas_rondas(self) -> bool:
        return len(self._partida.rondas) < self._partida.configuracion.numero_rondas
