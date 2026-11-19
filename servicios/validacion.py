from abc import ABC, abstractmethod
from typing import List
import re

from modelos.excepciones import PistaInvalidaException
from modelos.palabrasecreta import PalabraSecreta


class IValidadorPista(ABC):
    @abstractmethod
    def validar(self, pista, palabra_secreta: PalabraSecreta) -> bool:
        raise NotImplementedError


class ValidadorPalabraProhibida(IValidadorPista):
    def validar(self, pista, palabra_secreta: PalabraSecreta) -> bool:
        texto = " ".join(re.findall(r"[^\W_]+", PalabraSecreta.normalizar(pista.get_texto()), flags=re.UNICODE))
        palabra = " ".join(re.findall(r"[^\W_]+", PalabraSecreta.normalizar(palabra_secreta.texto), flags=re.UNICODE))
        if palabra and f" {palabra} " in f" {texto} ":
            raise PistaInvalidaException("La pista no puede contener la palabra secreta.")
        return True


class ValidadorLongitud(IValidadorPista):
    def __init__(self, longitud_maxima: int = 20):
        if not isinstance(longitud_maxima, int) or longitud_maxima < 1:
            raise ValueError("La longitud máxima debe ser mayor que cero.")
        self.longitud_maxima = longitud_maxima

    def validar(self, pista, palabra_secreta: PalabraSecreta) -> bool:
        texto_limpio = pista.get_texto().strip()
        if not texto_limpio:
            raise PistaInvalidaException("La pista no puede estar vacía.")
        if len(texto_limpio) > self.longitud_maxima:
            raise PistaInvalidaException(f"La pista supera los {self.longitud_maxima} caracteres.")
        return True


class ValidadorPistaCompuesto(IValidadorPista):
    def __init__(self, validadores: List[IValidadorPista]):
        self._validadores = list(validadores)

    def agregar(self, validador: IValidadorPista) -> None:
        if not isinstance(validador, IValidadorPista):
            raise TypeError("El validador debe implementar IValidadorPista.")
        self._validadores.append(validador)

    def validar(self, pista, palabra_secreta: PalabraSecreta) -> bool:
        for validador in self._validadores:
            validador.validar(pista, palabra_secreta)
        return True
