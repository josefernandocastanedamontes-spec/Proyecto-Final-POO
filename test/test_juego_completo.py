import unittest

from controladores.controlador_partida import ControladorPartida
from modelos.categoria import Categoria
from modelos.configuracionpartida import ConfiguracionPartida
from modelos.civil import Civil
from modelos.enumeraciones import EstadoJugador, FaseJuego
from modelos.excepciones import (
    BancoPalabrasVacioException, ConfiguracionInvalidaException,
    FaseInvalidaException, PistaInvalidaException, RegistroJugadorException,
    VotoInvalidoException,
)
from modelos.impostor import Impostor
from modelos.jugador import Jugador
from modelos.palabrasecreta import PalabraSecreta
from modelos.pista import Pista
from modelos.ronda import Ronda
from modelos.voto import Voto
from servicios.asignacion import AsignadorRolesAleatorio
from servicios.conteo import ContadorVotosMayoria
from servicios.palabras import RepositorioPalabrasMemoria
from servicios.validacion import (
    ValidadorLongitud, ValidadorPalabraProhibida, ValidadorPistaCompuesto,
)


class TestModelos(unittest.TestCase):
    def setUp(self):
        self.categoria = Categoria("Animales")
        self.palabra = PalabraSecreta("Gato", self.categoria)

    def test_palabra_compara_sin_distinguir_mayusculas_ni_espacios(self):
        self.assertTrue(self.palabra.coincide_con("  GATO "))
        self.assertFalse(self.palabra.coincide_con("perro"))

    def test_impostor_tiene_un_solo_intento_y_compara_respuesta(self):
        impostor = Impostor()
        self.assertFalse(impostor.conoce_palabra())
        self.assertFalse(impostor.intentar_adivinar("Perro", self.palabra))
        self.assertFalse(impostor.intento_disponible)
        self.assertFalse(impostor.intentar_adivinar("Gato", self.palabra))

    def test_impostor_no_recibe_palabra_en_mensaje_privado(self):
        self.assertNotIn("Gato", Impostor().obtener_palabra_visible())

    def test_civil_conoce_palabra(self):
        civil = Civil(self.palabra)
        self.assertTrue(civil.conoce_palabra())
        self.assertIn("Gato", civil.obtener_palabra_visible())

    def test_configuracion_rechaza_tiempo_negativo(self):
        with self.assertRaises(ConfiguracionInvalidaException):
            ConfiguracionPartida(2, -1, self.categoria, True, 20)

    def test_jugador_no_puede_votar_por_si_mismo(self):
        jugador = Jugador(1, "Ana")
        with self.assertRaises(VotoInvalidoException):
            jugador.votar(jugador)

    def test_jugador_eliminado_no_puede_votar(self):
        a, b = Jugador(1, "Ana"), Jugador(2, "Luis")
        a.estado = EstadoJugador.ELIMINADO
        with self.assertRaises(VotoInvalidoException):
            a.votar(b)

    def test_ronda_no_acepta_pistas_fuera_de_fase(self):
        with self.assertRaises(FaseInvalidaException):
            Ronda(1).registrar_pista(Pista(Jugador(1, "Ana"), "Miau", 1))

    def test_ronda_rechaza_pista_repetida_de_un_mismo_jugador(self):
        ronda = Ronda(1)
        ronda.avanzar_fase(FaseJuego.REVELACION)
        ronda.avanzar_fase(FaseJuego.PISTAS)
        jugador = Jugador(1, "Ana")
        ronda.registrar_pista(Pista(jugador, "Miau", 1))
        with self.assertRaises(PistaInvalidaException):
            ronda.registrar_pista(Pista(jugador, "Mascota", 2))


class TestServicios(unittest.TestCase):
    def setUp(self):
        self.categoria = Categoria("Lugares")
        self.palabra = PalabraSecreta("Playa", self.categoria)
        self.autor = Jugador(1, "Diana")

    def test_asignador_crea_exactamente_un_impostor_y_resto_civiles(self):
        jugadores = [Jugador(i, f"Jugador {i}") for i in range(1, 6)]
        AsignadorRolesAleatorio().asignar_roles(jugadores, self.palabra)
        roles = [j.rol.nombre for j in jugadores]
        self.assertEqual(roles.count("Impostor"), 1)
        self.assertEqual(roles.count("Civil"), 4)

    def test_asignador_rechaza_fuera_del_rango_de_jugadores(self):
        with self.assertRaises(ValueError):
            AsignadorRolesAleatorio().asignar_roles([self.autor, Jugador(2, "Luis")], self.palabra)

    def test_repositorio_busca_categoria_sin_distinguir_mayusculas(self):
        palabra = RepositorioPalabrasMemoria().obtener_palabra_aleatoria(Categoria("cOmIdA"))
        self.assertEqual(palabra.categoria.obtener_nombre(), "cOmIdA")

    def test_repositorio_rechaza_categoria_desconocida(self):
        with self.assertRaises(BancoPalabrasVacioException):
            RepositorioPalabrasMemoria().obtener_palabra_aleatoria(Categoria("Desconocida"))

    def test_validador_acepta_pista_valida(self):
        validador = ValidadorPistaCompuesto([ValidadorPalabraProhibida(), ValidadorLongitud(20)])
        self.assertTrue(validador.validar(Pista(self.autor, "Arena dorada", 1), self.palabra))

    def test_validador_rechaza_palabra_secreta(self):
        with self.assertRaises(PistaInvalidaException):
            ValidadorPalabraProhibida().validar(Pista(self.autor, "La playa es bonita", 1), self.palabra)

    def test_validador_no_rechaza_palabra_como_parte_de_otra(self):
        palabra = PalabraSecreta("Mar", self.categoria)
        self.assertTrue(ValidadorPalabraProhibida().validar(Pista(self.autor, "Maravilloso", 1), palabra))

    def test_validador_rechaza_pista_vacia_y_larga(self):
        validador = ValidadorLongitud(10)
        with self.assertRaises(PistaInvalidaException):
            validador.validar(Pista(self.autor, "   ", 1), self.palabra)
        with self.assertRaises(PistaInvalidaException):
            validador.validar(Pista(self.autor, "Demasiado extensa", 1), self.palabra)


class TestFlujoPartida(unittest.TestCase):
    def _preparar_partida_hasta_votacion(self, ultima=True, rondas=1):
        controlador = ControladorPartida()
        controlador.iniciar_partida(
            ["Ana", "Luis", "Marta", "Pedro"], rondas, 0, "Animales", ultima, 30
        )
        for jugador in controlador.jugadores:
            self.assertTrue(controlador.informacion_privada(jugador))
        controlador.confirmar_revelacion()
        for _ in range(len(controlador.jugadores)):
            controlador.registrar_pista("Miau")
        self.assertIs(controlador.ronda.fase, FaseJuego.DEBATE)
        controlador.finalizar_debate()
        self.assertIs(controlador.ronda.fase, FaseJuego.VOTACION)
        return controlador

    def test_partida_completa_civiles_descubren_impostor_y_fallan_ultima(self):
        controlador = self._preparar_partida_hasta_votacion(ultima=True)
        impostor = next(j for j in controlador.jugadores if j.rol.nombre == "Impostor")
        civil = next(j for j in controlador.jugadores if j is not impostor)
        respuesta = None
        for votante in controlador.jugadores:
            objetivo = impostor if votante is not impostor else civil
            respuesta = controlador.registrar_voto(votante, objetivo)
        self.assertEqual(respuesta["estado"], "ultima_oportunidad")
        resultado = controlador.resolver_ultima_oportunidad("respuesta incorrecta")
        self.assertEqual(resultado.ganador, "Civiles")
        self.assertEqual(len(resultado.roles_revelados), 4)

    def test_partida_gana_impostor_si_acusan_a_un_civil(self):
        controlador = self._preparar_partida_hasta_votacion(ultima=False)
        impostor = next(j for j in controlador.jugadores if j.rol.nombre == "Impostor")
        civil = next(j for j in controlador.jugadores if j is not impostor)
        respuesta = None
        for votante in controlador.jugadores:
            objetivo = civil if votante is not civil else impostor
            respuesta = controlador.registrar_voto(votante, objetivo)
        self.assertEqual(respuesta["estado"], "resultado")
        self.assertEqual(respuesta["resultado"].ganador, "Impostor")

    def test_partida_gana_impostor_si_adivina_correctamente(self):
        controlador = self._preparar_partida_hasta_votacion(ultima=True)
        impostor = next(j for j in controlador.jugadores if j.rol.nombre == "Impostor")
        civil = next(j for j in controlador.jugadores if j is not impostor)
        palabra = controlador.partida.palabra_secreta.texto
        for votante in controlador.jugadores:
            objetivo = impostor if votante is not impostor else civil
            controlador.registrar_voto(votante, objetivo)
        resultado = controlador.resolver_ultima_oportunidad(palabra)
        self.assertEqual(resultado.ganador, "Impostor")

    def test_registro_rechaza_nombres_duplicados(self):
        controlador = ControladorPartida()
        with self.assertRaises(RegistroJugadorException):
            controlador.iniciar_partida(["Ana", "ana", "Luis"], 1, 0, "Lugares")

    def test_siguiente_ronda_conserva_marcador(self):
        controlador = self._preparar_partida_hasta_votacion(ultima=False, rondas=2)
        impostor = next(j for j in controlador.jugadores if j.rol.nombre == "Impostor")
        civil = next(j for j in controlador.jugadores if j is not impostor)
        for votante in controlador.jugadores:
            controlador.registrar_voto(votante, impostor if votante is not impostor else civil)
        marcador_antes = controlador.partida.marcador
        controlador.siguiente_ronda()
        self.assertEqual(controlador.partida.marcador, marcador_antes)
        self.assertEqual(controlador.ronda.numero, 2)

    def test_empate_se_resuelve_con_segunda_votacion_y_puede_persistir(self):
        controlador = self._preparar_partida_hasta_votacion(ultima=False)
        a, b, c, d = controlador.jugadores
        for votante, objetivo in [(a, b), (b, a), (c, a), (d, b)]:
            respuesta = controlador.registrar_voto(votante, objetivo)
        self.assertEqual(respuesta["estado"], "desempate")
        self.assertEqual(set(respuesta["candidatos"]), {a, b})
        for votante, objetivo in [(a, b), (b, a), (c, a), (d, b)]:
            respuesta = controlador.registrar_voto_desempate(votante, objetivo)
        self.assertEqual(respuesta["estado"], "resultado")
        self.assertEqual(respuesta["resultado"].ganador, "Impostor")

    def test_controlador_no_permite_voto_repetido(self):
        controlador = self._preparar_partida_hasta_votacion(ultima=False)
        a, b, c, _ = controlador.jugadores
        controlador.registrar_voto(a, b)
        with self.assertRaises(VotoInvalidoException):
            controlador.registrar_voto(a, c)


if __name__ == "__main__":
    unittest.main(verbosity=2)
