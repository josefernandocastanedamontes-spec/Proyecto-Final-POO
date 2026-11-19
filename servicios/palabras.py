import random
from abc import ABC, abstractmethod
from modelos.palabrasecreta import PalabraSecreta
from modelos.categoria import Categoria


class IRepositorioPalabras(ABC):
    @abstractmethod
    def obtener_palabra_aleatoria(self, categoria: Categoria) -> PalabraSecreta:
        raise NotImplementedError

    @abstractmethod
    def obtener_categorias_disponibles(self) -> list:
        raise NotImplementedError


class RepositorioPalabrasMemoria(IRepositorioPalabras):
    def __init__(self):
        self.banco_palabras = {
            "Lugares": ["Playa", "Montaña", "Hospital", "Cine", "Parque", "Aeropuerto", "Museo", "Colegio"],
            "Comida": ["Pizza", "Hamburguesa", "Sushi", "Ensalada", "Helado", "Tacos", "Pasta", "Ceviche"],
            "Animales": ["Perro", "Gato", "Elefante", "Tigre", "Delfin", "Leon", "Jirafa", "Pinguino"],
        }

    def obtener_palabra_aleatoria(self, categoria: Categoria) -> PalabraSecreta:
        nombre_cat = categoria.obtener_nombre().strip().casefold()
        nombre_real = next((n for n in self.banco_palabras if n.casefold() == nombre_cat), None)
        if nombre_real is None:
            raise ValueError(f"La categoria '{categoria.obtener_nombre()}' no existe en el repositorio.")
        return PalabraSecreta(random.choice(self.banco_palabras[nombre_real]), categoria)

    def obtener_categorias_disponibles(self) -> list:
        return list(self.banco_palabras.keys())
