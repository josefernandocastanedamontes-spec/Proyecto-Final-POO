from abc import ABC, abstractmethod

class Rol(ABC):
    def __init__(self, nombre: str):
        self._nombre = nombre

    @property
    def nombre(self) -> str:
        return self._nombre

    @abstractmethod
    def conoce_palabra(self) -> bool:
        pass

    @abstractmethod
    def obtener_palabra_visible(self) -> str:
        pass

    @abstractmethod
    def intentar_adivinar(self, t: str) -> bool:
        pass