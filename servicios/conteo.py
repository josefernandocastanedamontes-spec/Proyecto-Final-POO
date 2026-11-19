from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class ResultadoVotacion:
    acusado: object = None
    empatados: Tuple[object, ...] = ()
    votos_maximos: int = 0

    @property
    def hay_empate(self) -> bool:
        return len(self.empatados) > 1

    @property
    def sin_votos(self) -> bool:
        return self.votos_maximos == 0


class IContadorVotos(ABC):
    @abstractmethod
    def contar_votos(self, votos: List) -> ResultadoVotacion:
        raise NotImplementedError


class ContadorVotosMayoria(IContadorVotos):
    """Devuelve el candidato más votado y señala expresamente los empates."""

    def contar_votos(self, votos: List) -> ResultadoVotacion:
        if not votos:
            return ResultadoVotacion()
        conteo = Counter(voto.acusado for voto in votos)
        max_votos = max(conteo.values())
        mas_votados = tuple(jugador for jugador, cantidad in conteo.items() if cantidad == max_votos)
        if len(mas_votados) > 1:
            return ResultadoVotacion(empatados=mas_votados, votos_maximos=max_votos)
        return ResultadoVotacion(acusado=mas_votados[0], votos_maximos=max_votos)
