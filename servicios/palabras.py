import random
from abc import ABC, abstractmethod
from modelos.palabrasecreta import PalabraSecreta
from modelos.categoria import Categoria

class IRepositorioPalabras(ABC):
    @abstractmethod
    def obtener_palabra_aleatoria(self, categoria: Categoria) -> PalabraSecreta:
        pass

class RepositorioPalabrasMemoria(IRepositorioPalabras):
    def __init__(self):
        # Banco de palabras organizado por las 3 categorías exactas
        self.banco_palabras = {
            "Lugares": ["Playa", "Montaña", "Hospital", "Cine", "Parque", "Aeropuerto", "Museo", "Colegio"],
            "Comida": ["Pizza", "Hamburguesa", "Sushi", "Ensalada", "Helado", "Tacos", "Pasta", "Ceviche"],
            "Animales": ["Perro", "Gato", "Elefante", "Tigre", "Delfin", "Leon", "Jirafa", "Pinguino"]
        }
        
    def obtener_palabra_aleatoria(self, categoria: Categoria) -> PalabraSecreta:
        # capitalizze() asegura que "comida" o "COMIDA" se convierta en "Comida" para buscar en el diccionario
        nombre_cat = categoria.obtener_nombre().capitalize()
        
        if nombre_cat not in self.banco_palabras:
            raise ValueError(f"La categoría '{nombre_cat}' no existe en el repositorio.")
            
        # Selecciona aleatoriamente una palabra de la lista correspondiente
        texto_aleatorio = random.choice(self.banco_palabras[nombre_cat])
        
        return PalabraSecreta(texto_aleatorio, categoria)
        
    def obtener_categorias_disponibles(self) -> list:
        """Método útil para que la interfaz gráfica sepa qué categorías mostrar en un menú."""
        return list(self.banco_palabras.keys())