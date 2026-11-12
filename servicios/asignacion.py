import random
from abc import ABC, abstractmethod
from typing import List

class IAsignadorRoles(ABC):
    @abstractmethod
    def asignar_roles(self, jugadores: List, palabra) -> None:
        pass

class AsignadorRolesAleatorio(IAsignadorRoles):
    def asignar_roles(self, jugadores: List, palabra) -> None:
        if not jugadores or len(jugadores) < 3:
            raise ValueError("Se requieren al menos 3 jugadores para iniciar la partida.")
        
        from modelos.impostor import Impostor
        from modelos.civil import Civil
        
        random.shuffle(jugadores)
        jugadores[0].rol = Impostor()
        
        for jugador in jugadores[1:]:
            jugador.rol = Civil(palabra)