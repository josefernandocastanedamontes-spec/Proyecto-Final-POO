import re
from abc import ABC, abstractmethod
from typing import List
from modelos.excepciones import PistaInvalidaException


class IValidadorPista(ABC):
    @abstractmethod
    def validar(self, pista, palabra_secreta) -> bool:
        pass


class ValidadorPalabraProhibida(IValidadorPista):
    def validar(self, pista, palabra_secreta) -> bool:
        palabra = palabra_secreta.texto.strip()
        texto = pista.get_texto()
        # Se compara la palabra completa, no fragmentos dentro de otras palabras.
        patron = rf"(?<!\\w){re.escape(palabra)}(?!\\w)"
        if re.search(patron, texto, flags=re.IGNORECASE):
            raise PistaInvalidaException("La pista no puede contener la palabra secreta.")
        return True


class ValidadorLongitud(IValidadorPista):
    def __init__(self, longitud_maxima: int = 20):
        if longitud_maxima < 1:
            raise ValueError("La longitud máxima debe ser mayor que cero.")
        self.longitud_maxima = longitud_maxima

    def validar(self, pista, palabra_secreta) -> bool:
        texto_limpio = pista.get_texto().strip()
        if len(texto_limpio) == 0:
            raise PistaInvalidaException("La pista no puede estar vacía.")
        if len(texto_limpio) > self.longitud_maxima:
            raise PistaInvalidaException(f"La pista supera los {self.longitud_maxima} caracteres.")
        return True


class ValidadorPistaCompuesto(IValidadorPista):
    def __init__(self, validadores: List[IValidadorPista]):
        self.validadores = validadores

    def validar(self, pista, palabra_secreta) -> bool:
        for validador in self.validadores:
            validador.validar(pista, palabra_secreta)
        return True
