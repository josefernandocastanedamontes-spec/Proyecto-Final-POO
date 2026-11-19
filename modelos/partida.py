from typing import List, Optional
from modelos.jugador import Jugador
from modelos.ronda import Ronda
from modelos.palabrasecreta import PalabraSecreta
from modelos.configuracionpartida import ConfiguracionPartida
from modelos.resultadopartida import ResultadoPartida


class Partida:
    def __init__(self, jugadores: List[Jugador], configuracion: ConfiguracionPartida):
        self._jugadores = list(jugadores)
        self._rondas: List[Ronda] = []
        self._palabra_secreta: Optional[PalabraSecreta] = None
        self._configuracion = configuracion
        self._resultados: List[ResultadoPartida] = []

    @property
    def jugadores(self) -> List[Jugador]:
        return list(self._jugadores)

    @property
    def rondas(self) -> List[Ronda]:
        return list(self._rondas)

    @property
    def palabra_secreta(self) -> Optional[PalabraSecreta]:
        return self._palabra_secreta

    @palabra_secreta.setter
    def palabra_secreta(self, palabra: PalabraSecreta) -> None:
        self._palabra_secreta = palabra

    @property
    def configuracion(self) -> ConfiguracionPartida:
        return self._configuracion

    @property
    def resultados(self) -> List[ResultadoPartida]:
        return list(self._resultados)

    def iniciar(self) -> None:
        self._rondas.clear()
        self._resultados.clear()
        self._palabra_secreta = None

    def nueva_ronda(self) -> Ronda:
        if len(self._rondas) >= self._configuracion.numero_rondas:
            raise ValueError("Se alcanzo el numero maximo de rondas configurado.")
        nueva = Ronda(numero=len(self._rondas) + 1)
        self._rondas.append(nueva)
        return nueva

    def registrar_resultado(self, resultado: ResultadoPartida) -> None:
        if not self._rondas:
            raise ValueError("No hay una ronda activa para registrar el resultado.")
        self._rondas[-1].registrar_resultado(resultado)
        self._resultados.append(resultado)

    def determinar_ganador(self) -> Optional[ResultadoPartida]:
        """Devuelve el resultado de la ultima ronda cerrada, si existe."""
        return self._resultados[-1] if self._resultados else None
