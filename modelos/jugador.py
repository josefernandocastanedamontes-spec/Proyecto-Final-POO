from typing import Optional

from modelos.rol import Rol
from modelos.enumeraciones import EstadoJugador
from modelos.pista import Pista
from modelos.voto import Voto
from modelos.excepciones import VotoInvalidoException


class Jugador:
    def __init__(self, id_jugador: int, nombre: str):
        nombre_limpio = nombre.strip() if isinstance(nombre, str) else ""
        if not nombre_limpio:
            raise ValueError("El nombre del jugador es obligatorio.")
        self._id = id_jugador
        self._nombre = nombre_limpio
        self._rol: Optional[Rol] = None
        self._estado = EstadoJugador.ACTIVO

    @property
    def id(self) -> int:
        return self._id

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def rol(self) -> Optional[Rol]:
        return self._rol

    @rol.setter
    def rol(self, nuevo_rol: Rol) -> None:
        if not isinstance(nuevo_rol, Rol):
            raise TypeError("El rol asignado debe ser una instancia de Rol.")
        self._rol = nuevo_rol

    @property
    def estado(self) -> EstadoJugador:
        return self._estado

    @estado.setter
    def estado(self, nuevo_estado: EstadoJugador) -> None:
        if not isinstance(nuevo_estado, EstadoJugador):
            raise TypeError("El estado debe pertenecer a EstadoJugador.")
        self._estado = nuevo_estado

    def dar_pista(self, texto: str, numero_turno: int = 0) -> Pista:
        if self._estado is not EstadoJugador.ACTIVO:
            raise ValueError("Un jugador eliminado no puede dar pistas.")
        return Pista(autor=self, texto=texto, numero_turno=numero_turno)

    def votar(self, acusado: "Jugador") -> Voto:
        if self._estado is not EstadoJugador.ACTIVO:
            raise VotoInvalidoException("Un jugador eliminado no puede votar.")
        if acusado is self:
            raise VotoInvalidoException("No puedes votar por ti mismo.")
        if not isinstance(acusado, Jugador):
            raise VotoInvalidoException("Debes seleccionar un jugador válido.")
        if acusado.estado is not EstadoJugador.ACTIVO:
            raise VotoInvalidoException("No puedes votar por un jugador eliminado.")
        return Voto(votante=self, acusado=acusado)
