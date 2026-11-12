import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from modelos.jugador import Jugador
from modelos.categoria import Categoria
from modelos.palabrasecreta import PalabraSecreta
from modelos.pista import Pista
from modelos.voto import Voto
from modelos.excepciones import PistaInvalidaException

from servicios.asignacion import AsignadorRolesAleatorio
from servicios.palabras import RepositorioPalabrasMemoria
from servicios.conteo import ContadorVotosMayoria
from servicios.validacion import (
    ValidadorPalabraProhibida, 
    ValidadorLongitud, 
    ValidadorPistaCompuesto
)


class TestServiciosJuego(unittest.TestCase):

    def test_asignador_roles_aleatorio(self):
        jugadores = [Jugador(1, "Ana"), Jugador(2, "Juan"), Jugador(3, "Pedro")]
        cat = Categoria("Animales")
        palabra = PalabraSecreta("Gato", cat)
        
        asignador = AsignadorRolesAleatorio()
        asignador.asignar_roles(jugadores, palabra)
        
        roles_nombres = [j.rol.nombre for j in jugadores]
        self.assertEqual(roles_nombres.count("Impostor"), 1)
        self.assertEqual(roles_nombres.count("Civil"), 2)

    def test_repositorio_palabras_por_categorias(self):
        repo = RepositorioPalabrasMemoria()
        
        cat_comida = Categoria("Comida")
        palabra_comida = repo.obtener_palabra_aleatoria(cat_comida)
        self.assertEqual(palabra_comida.categoria.obtener_nombre(), "Comida")
        
        cat_invalida = Categoria("Desconocida")
        with self.assertRaises(ValueError):
            repo.obtener_palabra_aleatoria(cat_invalida)

    def test_validador_pista_reglas(self):
        cat = Categoria("Lugares")
        palabra = PalabraSecreta("Playa", cat)
        autor = Jugador(1, "Diana")
        
        validador = ValidadorPistaCompuesto([
            ValidadorPalabraProhibida(),
            ValidadorLongitud(15)
        ])
        
        pista_ok = Pista(autor, "Arena", 1)
        self.assertTrue(validador.validar(pista_ok, palabra))
        
        pista_trampa = Pista(autor, "Voy a la playa", 1)
        with self.assertRaises(PistaInvalidaException):
            validador.validar(pista_trampa, palabra)
            
        pista_larga = Pista(autor, "Esta pista supera los quince caracteres", 1)
        with self.assertRaises(PistaInvalidaException):
            validador.validar(pista_larga, palabra)

    def test_contador_votos_mayoria(self):
        j1 = Jugador(1, "Carlos")
        j2 = Jugador(2, "Sofía")
        j3 = Jugador(3, "Mateo")
        
        votos = [
            Voto(j1, j2),
            Voto(j3, j2),
            Voto(j2, j1)
        ]
        
        contador = ContadorVotosMayoria()
        mas_votado = contador.contar_votos(votos)
        
        self.assertEqual(mas_votado, j2)


if __name__ == "__main__":
    unittest.main()