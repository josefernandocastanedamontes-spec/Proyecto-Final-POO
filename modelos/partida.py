from typing import List, Optional
from modelos.jugador import Jugador
from modelos.ronda import Ronda
from modelos.palabrasecreta import PalabraSecreta
from modelos.configuracionpartida import ConfiguracionPartida
from modelos.resultadopartida import ResultadoPartida

class Partida:
    def __init__(self, jugadores: List[Jugador], configuracion: ConfiguracionPartida):
        self._jugadores = jugadores
        self._rondas: List[Ronda] = []
        self._palabra_secreta: Optional[PalabraSecreta] = None
        self._configuracion = configuracion

    @property
    def jugadores(self) -> List[Jugador]: return self._jugadores
    @property
    def rondas(self) -> List[Ronda]: return self._rondas
    @property
    def palabra_secreta(self) -> Optional[PalabraSecreta]: return self._palabra_secreta
    @palabra_secreta.setter
    def palabra_secreta(self, palabra: PalabraSecreta): self._palabra_secreta = palabra

    def iniciar(self) -> None:
        self._rondas.clear()

    def nueva_ronda(self) -> Ronda:
        nueva = Ronda(numero=len(self._rondas) + 1)
        self._rondas.append(nueva)
        return nueva

    def determinar_ganador(self) -> ResultadoPartida:
        return ResultadoPartida("Pendiente", None, {})