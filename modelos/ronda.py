from typing import List
from modelos.enumeraciones import FaseJuego
from modelos.pista import Pista
from modelos.voto import Voto

class Ronda:
    def __init__(self, numero: int):
        self._numero = numero
        self._pistas: List[Pista] = []
        self._votos: List[Voto] = []
        self._fase = FaseJuego.ASIGNACION

    @property
    def numero(self) -> int: return self._numero
    @property
    def pistas(self) -> List[Pista]: return self._pistas
    @property
    def votos(self) -> List[Voto]: return self._votos
    @property
    def fase(self) -> FaseJuego: return self._fase

    def registrar_pista(self, p: Pista) -> None:
        self._pistas.append(p)

    def registrar_voto(self, v: Voto) -> None:
        self._votos.append(v)

    def avanzar_fase(self) -> None:
        pass