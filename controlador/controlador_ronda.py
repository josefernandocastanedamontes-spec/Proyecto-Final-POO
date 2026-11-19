# -*- coding: utf-8 -*-
from typing import Callable, List
from modelos.enumeraciones import EstadoJugador
from modelos.excepciones import PistaInvalidaException
from modelos.jugador import Jugador
from modelos.partida import Partida
from modelos.pista import Pista
from modelos.ronda import Ronda
from servicios.validacion import IValidadorPista
from vista.interfaces import IVistaJuego


class ControladorRonda:
    """Coordina la asignacion privada de roles, las pistas y el debate."""

    def __init__(self, vista: IVistaJuego, validador_pista: IValidadorPista):
        self._vista = vista
        self._validador_pista = validador_pista

    def iniciar_asignacion_roles(self, jugadores: List[Jugador], al_finalizar: Callable[[], None]) -> None:
        self._mostrar_turno_asignacion(jugadores, 0, al_finalizar)

    def _mostrar_turno_asignacion(self, jugadores: List[Jugador], indice: int,
                                  al_finalizar: Callable[[], None]) -> None:
        if indice >= len(jugadores):
            al_finalizar()
            return
        jugador = jugadores[indice]
        self._vista.mostrar_asignacion_privada(
            nombre_jugador=jugador.nombre,
            numero_jugador=indice + 1,
            total_jugadores=len(jugadores),
            obtener_texto_rol=lambda: jugador.rol.obtener_palabra_visible(),
            on_siguiente_jugador=lambda: self._mostrar_turno_asignacion(
                jugadores, indice + 1, al_finalizar
            ),
        )

    def iniciar_fase_pistas(self, partida: Partida, ronda: Ronda,
                            jugadores_ordenados: List[Jugador], longitud_maxima: int,
                            al_finalizar_pistas: Callable[[], None]) -> None:
        ronda.avanzar_fase()
        activos = [j for j in jugadores_ordenados if j.estado == EstadoJugador.ACTIVO]
        self._pedir_siguiente_pista(partida, ronda, activos, 0, longitud_maxima, al_finalizar_pistas)

    def _pedir_siguiente_pista(self, partida: Partida, ronda: Ronda,
                              activos: List[Jugador], indice: int, longitud_maxima: int,
                              al_finalizar_pistas: Callable[[], None]) -> None:
        if indice >= len(activos):
            al_finalizar_pistas()
            return
        jugador_actual = activos[indice]
        pistas_previas = [(p.get_autor().nombre, p.get_texto()) for p in ronda.pistas]
        categoria_nombre = partida.palabra_secreta.categoria.obtener_nombre()

        def procesar_pista(texto_pista: str) -> None:
            pista = Pista(autor=jugador_actual, texto=texto_pista.strip(), numero_turno=indice + 1)
            try:
                self._validador_pista.validar(pista, partida.palabra_secreta)
                ronda.registrar_pista(pista)
                self._pedir_siguiente_pista(
                    partida, ronda, activos, indice + 1, longitud_maxima, al_finalizar_pistas
                )
            except (PistaInvalidaException, ValueError) as exc:
                self._vista.mostrar_error("Pista invalida", str(exc))

        self._vista.mostrar_turno_pista(
            numero_ronda=ronda.numero,
            categoria=categoria_nombre,
            nombre_jugador=jugador_actual.nombre,
            pistas_previas=pistas_previas,
            longitud_maxima=longitud_maxima,
            on_enviar_pista=procesar_pista,
        )

    def iniciar_fase_debate(self, partida: Partida, ronda: Ronda, segundos_debate: int,
                            al_finalizar_debate: Callable[[], None]) -> None:
        ronda.avanzar_fase()
        pistas_ronda = [(p.get_autor().nombre, p.get_texto()) for p in ronda.pistas]
        categoria_nombre = partida.palabra_secreta.categoria.obtener_nombre()
        self._vista.mostrar_debate(
            numero_ronda=ronda.numero,
            categoria=categoria_nombre,
            pistas_ronda=pistas_ronda,
            segundos_debate=segundos_debate,
            on_finalizar_debate=al_finalizar_debate,
        )
