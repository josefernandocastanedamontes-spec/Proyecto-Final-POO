from abc import ABC, abstractmethod
from typing import List, Optional

class IContadorVotos(ABC):
    @abstractmethod
    def contar_votos(self, votos: List) -> Optional[object]:
        pass

class ContadorVotosMayoria(IContadorVotos):
    def contar_votos(self, votos: List) -> Optional[object]:
        if not votos:
            return None
            
        conteo = {}
        for voto in votos:
            acusado = voto.get_acusado()
            conteo[acusado] = conteo.get(acusado, 0) + 1
                
        max_votos = max(conteo.values())
        mas_votados = [jugador for jugador, cant in conteo.items() if cant == max_votos]
        
        if len(mas_votados) > 1:
            return None 
            
        return mas_votados[0]