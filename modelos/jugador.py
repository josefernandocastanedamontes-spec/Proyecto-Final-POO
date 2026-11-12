from typing import Optional

from modelos.rol import Rol

from modelos.enumeraciones import EstadoJugador

from modelos.pista import Pista

from modelos.voto import Voto

class Jugador:
    
    def __init__(self, id_jugador: int, nombre: str):
        
        self._id = id_jugador
        self._nombre = nombre
        self._rol: Optional[Rol] = None
        self._estado = EstadoJugador.ACTIVO

    @property
    def id(self) -> int: return self._id
    
    @property
    def nombre(self) -> str: return self._nombre
    
    @property
    def rol(self) -> Optional[Rol]: return self._rol
    
    @rol.setter
    def rol(self, nuevo_rol: Rol): self._rol = nuevo_rol
    
    @property
    def estado(self) -> EstadoJugador: return self._estado
    
    @estado.setter
    def estado(self, nuevo_estado: EstadoJugador): self._estado = nuevo_estado

    def dar_pista(self, texto: str) -> Pista:
        return Pista(autor=self, texto=texto, numero_turno=0)

    def votar(self, acusado: 'Jugador') -> Voto:
        return Voto(votante=self, acusado=acusado)