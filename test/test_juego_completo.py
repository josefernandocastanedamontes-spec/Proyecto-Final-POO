import unittest

from modelos.categoria import Categoria
from modelos.jugador import Jugador
from modelos.palabrasecreta import PalabraSecreta
from modelos.pista import Pista
from modelos.voto import Voto
from modelos.excepciones import PistaInvalidaException
from servicios.asignacion import AsignadorRolesAleatorio
from servicios.conteo import ContadorVotosMayoria
from servicios.palabras import RepositorioPalabrasMemoria
from servicios.validacion import (
    ValidadorLongitud,
    ValidadorPalabraProhibida,
    ValidadorPistaCompuesto,
)


class TestServiciosJuego(unittest.TestCase):
    def test_asignador_crea_un_impostor(self):
        jugadores = [Jugador(1, "Ana"), Jugador(2, "Juan"), Jugador(3, "Pedro")]
        palabra = PalabraSecreta("Gato", Categoria("Animales"))
        AsignadorRolesAleatorio().asignar_roles(jugadores, palabra)
        roles = [j.rol.nombre for j in jugadores]
        self.assertEqual(roles.count("Impostor"), 1)
        self.assertEqual(roles.count("Civil"), 2)

    def test_repositorio_reconoce_categoria(self):
        repo = RepositorioPalabrasMemoria()
        palabra = repo.obtener_palabra_aleatoria(Categoria("comida"))
        self.assertEqual(palabra.categoria.obtener_nombre(), "comida")
        with self.assertRaises(ValueError):
            repo.obtener_palabra_aleatoria(Categoria("Inexistente"))

    def test_validador_compuesto_rechaza_vacia_y_larga(self):
        palabra = PalabraSecreta("Playa", Categoria("Lugares"))
        autor = Jugador(1, "Diana")
        validador = ValidadorPistaCompuesto([ValidadorLongitud(15), ValidadorPalabraProhibida()])
        self.assertTrue(validador.validar(Pista(autor, "Arena", 1), palabra))
        with self.assertRaises(PistaInvalidaException):
            validador.validar(Pista(autor, "   ", 2), palabra)
        with self.assertRaises(PistaInvalidaException):
            validador.validar(Pista(autor, "Una pista demasiado larga", 3), palabra)

    def test_contador_retorna_mayoria_unica_y_expone_empate(self):
        a, b, c, d = [Jugador(i, n) for i, n in enumerate(("A", "B", "C", "D"), 1)]
        contador = ContadorVotosMayoria()
        self.assertIs(contador.contar_votos([Voto(a, b), Voto(c, b), Voto(b, a)]), b)
        votos = [Voto(a, b), Voto(b, a), Voto(c, a), Voto(d, b)]
        self.assertIsNone(contador.contar_votos(votos))
        self.assertEqual(set(contador.obtener_candidatos_empatados(votos)), {a, b})


if __name__ == "__main__":
    unittest.main()
