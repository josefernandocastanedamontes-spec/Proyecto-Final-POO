import random
from abc import ABC, abstractmethod
from typing import List, Optional


class IAsignadorRoles(ABC):
    @abstractmethod
    def asignar_roles(self, jugadores: List, palabra) -> None:
        raise NotImplementedError


class AsignadorRolesAleatorio(IAsignadorRoles):
    def __init__(self, generador: Optional[random.Random] = None):
        self._generador = generador or random.Random()

    def asignar_roles(self, jugadores: List, palabra) -> None:
        if not 3 <= len(jugadores) <= 10:
            raise ValueError("Se requieren entre 3 y 10 jugadores para iniciar la partida.")
        from modelos.impostor import Impostor
        from modelos.civil import Civil

        impostor = self._generador.choice(jugadores)
        for jugador in jugadores:
            jugador.rol = Impostor() if jugador is impostor else Civil(palabra)
