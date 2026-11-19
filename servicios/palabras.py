import random
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from modelos.palabrasecreta import PalabraSecreta
from modelos.categoria import Categoria
from modelos.excepciones import BancoPalabrasVacioException


class IRepositorioPalabras(ABC):
    @abstractmethod
    def obtener_palabra_aleatoria(self, categoria: Categoria) -> PalabraSecreta:
        raise NotImplementedError


class RepositorioPalabrasMemoria(IRepositorioPalabras):
    def __init__(self, banco_palabras: Optional[Dict[str, List[str]]] = None,
                 generador: Optional[random.Random] = None):
        self._banco_palabras = banco_palabras or {
            "Lugares": ["Playa", "Montaña", "Hospital", "Cine", "Parque", "Aeropuerto", "Museo", "Colegio"],
            "Comida": ["Pizza", "Hamburguesa", "Sushi", "Ensalada", "Helado", "Tacos", "Pasta", "Ceviche"],
            "Animales": ["Perro", "Gato", "Elefante", "Tigre", "Delfín", "León", "Jirafa", "Pingüino"],
        }
        self._generador = generador or random.Random()

    def obtener_palabra_aleatoria(self, categoria: Categoria) -> PalabraSecreta:
        nombre_cat = categoria.obtener_nombre().strip().casefold()
        coincidencia = next((k for k in self._banco_palabras if k.casefold() == nombre_cat), None)
        if coincidencia is None:
            raise BancoPalabrasVacioException(f"La categoría '{categoria}' no existe en el banco.")
        palabras = self._banco_palabras[coincidencia]
        if not palabras:
            raise BancoPalabrasVacioException(f"La categoría '{coincidencia}' no tiene palabras.")
        return PalabraSecreta(self._generador.choice(palabras), categoria)

    def obtener_categorias_disponibles(self) -> list:
        return list(self._banco_palabras.keys())
