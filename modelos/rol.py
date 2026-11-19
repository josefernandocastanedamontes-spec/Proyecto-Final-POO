from abc import ABC, abstractmethod
from typing import Optional

from modelos.palabrasecreta import PalabraSecreta


class Rol(ABC):
    def __init__(self, nombre: str):
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        return self._nombre

    @abstractmethod
    def conoce_palabra(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def obtener_palabra_visible(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def intentar_adivinar(self, texto: str, palabra_secreta: Optional[PalabraSecreta] = None) -> bool:
        """Aplica la regla del rol ante un intento de adivinanza."""
        raise NotImplementedError
