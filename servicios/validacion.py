import re
from abc import ABC, abstractmethod
from typing import List
from modelos.excepciones import PistaInvalidaException


class IValidadorPista(ABC):
    @abstractmethod
    def validar(self, pista, palabra_secreta) -> bool:
        raise NotImplementedError


class ValidadorPalabraProhibida(IValidadorPista):
    def validar(self, pista, palabra_secreta) -> bool:
        texto = pista.get_texto().strip()
        palabra = palabra_secreta.texto.strip()
        # Compara el termino completo y evita falsos positivos por subcadenas.
        patron = rf"(?<!\w){re.escape(palabra)}(?!\w)"
        if re.search(patron, texto, flags=re.IGNORECASE | re.UNICODE):
            raise PistaInvalidaException("La pista no puede contener la palabra secreta.")
        return True


class ValidadorLongitud(IValidadorPista):
    def __init__(self, longitud_maxima: int = 20):
        if longitud_maxima <= 0:
            raise ValueError("La longitud maxima debe ser mayor que cero.")
        self.longitud_maxima = longitud_maxima

    def validar(self, pista, palabra_secreta) -> bool:
        texto_limpio = pista.get_texto().strip()
        if not texto_limpio:
            raise PistaInvalidaException("La pista no puede estar vacia.")
        if len(texto_limpio) > self.longitud_maxima:
            raise PistaInvalidaException(f"La pista supera los {self.longitud_maxima} caracteres.")
        return True


class ValidadorPistaCompuesto(IValidadorPista):
    def __init__(self, validadores: List[IValidadorPista]):
        self.validadores = list(validadores)

    def validar(self, pista, palabra_secreta) -> bool:
        for validador in self.validadores:
            validador.validar(pista, palabra_secreta)
        return True
