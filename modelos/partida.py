from typing import Dict, List, Optional

from modelos.jugador import Jugador
from modelos.ronda import Ronda
from modelos.palabrasecreta import PalabraSecreta
from modelos.configuracionpartida import ConfiguracionPartida
from modelos.resultadopartida import ResultadoPartida
from modelos.enumeraciones import FaseJuego, EstadoJugador
from modelos.excepciones import RegistroJugadorException, FaseInvalidaException
from servicios.asignacion import AsignadorRolesAleatorio
from servicios.palabras import RepositorioPalabrasMemoria


class Partida:
    def __init__(self, jugadores: List[Jugador], configuracion: ConfiguracionPartida,
                 asignador=None, repositorio_palabras=None, contador_votos=None):
        self._jugadores = list(jugadores)
        self._rondas: List[Ronda] = []
        self._palabra_secreta: Optional[PalabraSecreta] = None
        self._configuracion = configuracion
        self._asignador = asignador or AsignadorRolesAleatorio()
        self._repositorio = repositorio_palabras or RepositorioPalabrasMemoria()
        self._contador_votos = contador_votos
        self._resultado_actual: Optional[ResultadoPartida] = None
        self._marcador: Dict[str, int] = {j.nombre: 0 for j in self._jugadores}
        self._iniciada = False

    @property
    def jugadores(self) -> List[Jugador]:
        return list(self._jugadores)

    @property
    def rondas(self) -> List[Ronda]:
        return list(self._rondas)

    @property
    def ronda_actual(self) -> Optional[Ronda]:
        return self._rondas[-1] if self._rondas else None

    @property
    def palabra_secreta(self) -> Optional[PalabraSecreta]:
        return self._palabra_secreta

    @property
    def configuracion(self) -> ConfiguracionPartida:
        return self._configuracion

    @property
    def resultado_actual(self) -> Optional[ResultadoPartida]:
        return self._resultado_actual

    @property
    def marcador(self) -> Dict[str, int]:
        return dict(self._marcador)

    def validar_jugadores(self) -> None:
        if not 3 <= len(self._jugadores) <= 10:
            raise RegistroJugadorException("La partida necesita entre 3 y 10 jugadores.")
        nombres = [j.nombre.casefold() for j in self._jugadores]
        if len(nombres) != len(set(nombres)):
            raise RegistroJugadorException("Los nombres de los jugadores deben ser únicos.")

    def iniciar(self) -> Ronda:
        if self._iniciada:
            raise FaseInvalidaException("La partida ya fue iniciada.")
        self.validar_jugadores()
        self._configuracion.validar()
        return self._crear_ronda()

    def _crear_ronda(self) -> Ronda:
        if len(self._rondas) >= self._configuracion.numero_rondas:
            raise FaseInvalidaException("Ya se completaron todas las rondas configuradas.")
        for jugador in self._jugadores:
            jugador.estado = EstadoJugador.ACTIVO
        self._palabra_secreta = self._repositorio.obtener_palabra_aleatoria(self._configuracion.categoria)
        self._asignador.asignar_roles(self._jugadores, self._palabra_secreta)
        nueva = Ronda(numero=len(self._rondas) + 1)
        self._rondas.append(nueva)
        self._iniciada = True
        self._resultado_actual = None
        return nueva

    def nueva_ronda(self) -> Ronda:
        if not self._iniciada or self.ronda_actual is None or self.ronda_actual.fase is not FaseJuego.RESULTADO:
            raise FaseInvalidaException("La ronda actual debe terminar antes de iniciar otra.")
        return self._crear_ronda()

    def determinar_ganador(self, acusado=None, empate: bool = False,
                           adivinanza: Optional[str] = None) -> ResultadoPartida:
        ronda = self.ronda_actual
        if ronda is None:
            raise FaseInvalidaException("No hay una ronda activa.")
        if self._resultado_actual is not None:
            raise FaseInvalidaException("La ronda ya tiene un resultado definitivo.")
        if ronda.fase not in (FaseJuego.VOTACION, FaseJuego.DESEMPATE, FaseJuego.RESULTADO):
            raise FaseInvalidaException("La votación todavía no puede resolverse.")
        impostor = next((j for j in self._jugadores if j.rol and j.rol.nombre == "Impostor"), None)
        motivo = ""
        if empate or acusado is None:
            ganador = "Impostor"
            motivo = "La votación terminó en empate; el impostor sobrevivió."
        elif acusado is impostor:
            if self._configuracion.ultima_oportunidad:
                acerto = impostor.rol.intentar_adivinar(adivinanza or "", self._palabra_secreta)
                if acerto:
                    ganador = "Impostor"
                    motivo = "El impostor acertó la última oportunidad."
                else:
                    ganador = "Civiles"
                    impostor.estado = EstadoJugador.ELIMINADO
                    motivo = "El impostor fue descubierto y no acertó la última oportunidad."
            else:
                ganador = "Civiles"
                impostor.estado = EstadoJugador.ELIMINADO
                motivo = "El impostor fue descubierto."
        else:
            ganador = "Impostor"
            acusado.estado = EstadoJugador.ELIMINADO
            motivo = f"El grupo acusó a {acusado.nombre}, que era civil."
        roles = {j.nombre: j.rol.nombre if j.rol else "Sin asignar" for j in self._jugadores}
        resultado = ResultadoPartida(ganador, acusado, roles, motivo)
        self._resultado_actual = resultado
        if ronda.fase is not FaseJuego.RESULTADO:
            ronda.avanzar_fase(FaseJuego.RESULTADO)
        if ganador == "Civiles":
            for jugador in self._jugadores:
                if jugador.rol and jugador.rol.nombre == "Civil":
                    self._marcador[jugador.nombre] += 1
        elif impostor:
            self._marcador[impostor.nombre] += 1
        return resultado
