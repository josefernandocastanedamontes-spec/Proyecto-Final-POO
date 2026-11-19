from typing import List, Optional
from modelos.enumeraciones import FaseJuego
from modelos.pista import Pista
from modelos.voto import Voto
from modelos.resultadopartida import ResultadoPartida


class Ronda:
    _TRANSICIONES = {
        FaseJuego.ASIGNACION: FaseJuego.PISTAS,
        FaseJuego.PISTAS: FaseJuego.DEBATE,
        FaseJuego.DEBATE: FaseJuego.VOTACION,
        FaseJuego.VOTACION: FaseJuego.RESULTADO,
    }

    def __init__(self, numero: int):
        if numero < 1:
            raise ValueError("El numero de ronda debe ser positivo.")
        self._numero = numero
        self._pistas: List[Pista] = []
        self._votos: List[Voto] = []
        self._votos_desempate: List[Voto] = []
        self._fase = FaseJuego.ASIGNACION
        self._resultado: Optional[ResultadoPartida] = None

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def pistas(self) -> List[Pista]:
        return list(self._pistas)

    @property
    def votos(self) -> List[Voto]:
        return list(self._votos)

    @property
    def votos_desempate(self) -> List[Voto]:
        return list(self._votos_desempate)

    @property
    def fase(self) -> FaseJuego:
        return self._fase

    @property
    def resultado(self) -> Optional[ResultadoPartida]:
        return self._resultado

    def avanzar_fase(self) -> FaseJuego:
        siguiente = self._TRANSICIONES.get(self._fase)
        if siguiente is None:
            raise ValueError("La ronda ya se encuentra en su fase final.")
        self._fase = siguiente
        return self._fase

    def registrar_pista(self, pista: Pista) -> None:
        if self._fase != FaseJuego.PISTAS:
            raise ValueError("No se pueden registrar pistas fuera de la fase de pistas.")
        if any(p.get_autor() == pista.get_autor() for p in self._pistas):
            raise ValueError("El jugador ya registro una pista en esta ronda.")
        self._pistas.append(pista)

    def registrar_voto(self, voto: Voto, desempate: bool = False) -> None:
        if self._fase != FaseJuego.VOTACION:
            raise ValueError("No se pueden registrar votos fuera de la fase de votacion.")
        destino = self._votos_desempate if desempate else self._votos
        if any(v.votante == voto.votante for v in destino):
            raise ValueError("El jugador ya voto en esta votacion.")
        if voto.votante == voto.get_acusado():
            raise ValueError("No se permite votar por uno mismo.")
        destino.append(voto)

    def registrar_resultado(self, resultado: ResultadoPartida) -> None:
        if self._fase == FaseJuego.VOTACION:
            self.avanzar_fase()
        if self._fase != FaseJuego.RESULTADO:
            raise ValueError("El resultado solo puede registrarse al finalizar la votacion.")
        self._resultado = resultado
