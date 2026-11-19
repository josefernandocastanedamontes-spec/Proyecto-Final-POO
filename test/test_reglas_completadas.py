import unittest

from modelos.categoria import Categoria
from modelos.configuracionpartida import ConfiguracionPartida
from modelos.enumeraciones import FaseJuego
from modelos.excepciones import PistaInvalidaException
from modelos.jugador import Jugador
from modelos.palabrasecreta import PalabraSecreta
from modelos.partida import Partida
from modelos.pista import Pista
from modelos.resultadopartida import ResultadoPartida
from modelos.ronda import Ronda
from modelos.voto import Voto
from servicios.conteo import ContadorVotosMayoria
from servicios.validacion import ValidadorPalabraProhibida
from controlador.controlador_votacion import ControladorVotacion


class VistaDobleVotacion:
    def __init__(self, elecciones):
        self.elecciones = list(elecciones)
        self.llamadas = []

    def mostrar_votacion_privada(self, numero_ronda, nombre_votante, candidatos,
                                 pistas_ronda, on_registrar_voto):
        self.llamadas.append((nombre_votante, list(candidatos)))
        on_registrar_voto(self.elecciones.pop(0))

    def mostrar_info(self, titulo, mensaje):
        pass

    def mostrar_error(self, titulo, mensaje):
        raise AssertionError(f"Error inesperado: {titulo}: {mensaje}")


class TestReglasCompletadas(unittest.TestCase):
    def test_ronda_avanza_por_fases_y_finaliza(self):
        ronda = Ronda(1)
        self.assertEqual(ronda.avanzar_fase(), FaseJuego.PISTAS)
        self.assertEqual(ronda.avanzar_fase(), FaseJuego.DEBATE)
        self.assertEqual(ronda.avanzar_fase(), FaseJuego.VOTACION)
        self.assertEqual(ronda.avanzar_fase(), FaseJuego.RESULTADO)
        with self.assertRaises(ValueError):
            ronda.avanzar_fase()

    def test_configuracion_rechaza_tiempo_fuera_de_rango(self):
        config = ConfiguracionPartida(2, 0, Categoria("Lugares"), True, 20)
        with self.assertRaises(ValueError):
            config.validar()

    def test_palabra_prohibida_compara_termino_completo(self):
        palabra = PalabraSecreta("Mar", Categoria("Lugares"))
        autor = Jugador(1, "Ana")
        validador = ValidadorPalabraProhibida()
        self.assertTrue(validador.validar(Pista(autor, "Maravilloso", 1), palabra))
        with self.assertRaises(PistaInvalidaException):
            validador.validar(Pista(autor, "Veo el MAR hoy", 2), palabra)

    def test_partida_guarda_resultado_de_ronda(self):
        jugadores = [Jugador(1, "Ana"), Jugador(2, "Luis"), Jugador(3, "Eva")]
        config = ConfiguracionPartida(2, 60, Categoria("Animales"), True, 20)
        partida = Partida(jugadores, config)
        partida.iniciar()
        ronda = partida.nueva_ronda()
        ronda.avanzar_fase()
        ronda.avanzar_fase()
        ronda.avanzar_fase()
        resultado = ResultadoPartida("Civiles", None, {})
        partida.registrar_resultado(resultado)
        self.assertIs(partida.determinar_ganador(), resultado)
        self.assertEqual(ronda.fase, FaseJuego.RESULTADO)

    def test_desempate_usa_solo_candidatos_empatados(self):
        jugadores = [Jugador(i, n) for i, n in enumerate(("Ana", "Bruno", "Carla", "Diego"), 1)]
        elecciones = ["Bruno", "Ana", "Ana", "Bruno", "Bruno", "Ana", "Ana", "Bruno"]
        vista = VistaDobleVotacion(elecciones)
        ronda = Ronda(1)
        ronda.avanzar_fase()
        ronda.avanzar_fase()
        resultado = []
        ControladorVotacion(vista, ContadorVotosMayoria()).iniciar_votacion(
            ronda, jugadores, resultado.append
        )
        self.assertEqual(len(vista.llamadas), 8)
        self.assertEqual(resultado, [None])
        self.assertNotIn("Ana", vista.llamadas[0][1])
        self.assertNotIn("Bruno", vista.llamadas[1][1])
        self.assertEqual(set(vista.llamadas[4][1]), {"Bruno"})
        self.assertEqual(set(vista.llamadas[5][1]), {"Ana"})
        self.assertEqual(len(ronda.votos), 4)
        self.assertEqual(len(ronda.votos_desempate), 4)


if __name__ == "__main__":
    unittest.main()
