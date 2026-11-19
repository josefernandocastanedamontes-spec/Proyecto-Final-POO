from typing import List
from modelos.enumeraciones import FaseJuego
from modelos.pista import Pista
from modelos.voto import Voto


class Ronda:
    """Representa una ronda y controla sus transiciones de fase."""

    _ORDEN_FASES = (
        FaseJuego.ASIGNACION,
        FaseJuego.PISTAS,
        FaseJuego.DEBATE,
        FaseJuego.VOTACION,
        FaseJuego.RESULTADO,
    )

    def __init__(self, numero: int):
        if numero < 1:
            raise ValueError("El número de ronda debe ser positivo.")
        self._numero = numero
        self._pistas: List[Pista] = []
        self._votos: List[Voto] = []
        self._fase = FaseJuego.ASIGNACION

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def pistas(self) -> List[Pista]:
        return self._pistas

    @property
    def votos(self) -> List[Voto]:
        return self._votos

    @property
    def fase(self) -> FaseJuego:
        return self._fase

    def registrar_pista(self, p: Pista) -> None:
        if self._fase not in (FaseJuego.ASIGNACION, FaseJuego.PISTAS):
            raise ValueError("No se pueden registrar pistas en esta fase.")
        self._pistas.append(p)
        self._fase = FaseJuego.PISTAS

    def registrar_voto(self, v: Voto) -> None:
        if self._fase not in (FaseJuego.DEBATE, FaseJuego.VOTACION):
            raise ValueError("No se pueden registrar votos en esta fase.")
        self._votos.append(v)
        self._fase = FaseJuego.VOTACION

    def avanzar_fase(self) -> FaseJuego:
        """Avanza una fase; RESULTADO es la fase terminal."""
        indice = self._ORDEN_FASES.index(self._fase)
        if indice == len(self._ORDEN_FASES) - 1:
            raise ValueError("La ronda ya se encuentra en su fase final.")
        self._fase = self._ORDEN_FASES[indice + 1]
        return self._fase

    def establecer_fase(self, fase: FaseJuego) -> None:
        if not isinstance(fase, FaseJuego):
            raise TypeError("La fase debe ser un valor de FaseJuego.")
        self._fase = fase
