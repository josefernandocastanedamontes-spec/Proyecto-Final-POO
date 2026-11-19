from abc import ABC, abstractmethod
from typing import List, Optional


class IContadorVotos(ABC):
    @abstractmethod
    def contar_votos(self, votos: List) -> Optional[object]:
        raise NotImplementedError

    @abstractmethod
    def obtener_candidatos_empatados(self, votos: List) -> List:
        raise NotImplementedError


class ContadorVotosMayoria(IContadorVotos):
    def obtener_candidatos_empatados(self, votos: List) -> List:
        if not votos:
            return []
        conteo = {}
        for voto in votos:
            acusado = voto.get_acusado()
            conteo[acusado] = conteo.get(acusado, 0) + 1
        max_votos = max(conteo.values())
        return [jugador for jugador, cantidad in conteo.items() if cantidad == max_votos]

    def contar_votos(self, votos: List) -> Optional[object]:
        candidatos = self.obtener_candidatos_empatados(votos)
        return candidatos[0] if len(candidatos) == 1 else None
