# -*- coding: utf-8 -*-
from typing import Callable, List, Optional
from modelos.enumeraciones import EstadoJugador, FaseJuego
from modelos.excepciones import VotoInvalidoException
from modelos.jugador import Jugador
from modelos.ronda import Ronda
from servicios.conteo import IContadorVotos
from vista.interfaces import IVistaJuego


class ControladorVotacion:
    """Coordina la votación secreta y el conteo de votos de la ronda."""

    def __init__(self, vista: IVistaJuego, contador_votos: IContadorVotos):
        self._vista = vista
        self._contador_votos = contador_votos

    def iniciar_votacion(
        self,
        ronda: Ronda,
        jugadores_ordenados: List[Jugador],
        al_finalizar_votacion: Callable[[Optional[Jugador]], None],
    ) -> None:
        ronda._fase = FaseJuego.VOTACION
        activos = [j for j in jugadores_ordenados if j.estado == EstadoJugador.ACTIVO]
        self._pedir_siguiente_voto(ronda, activos, 0, al_finalizar_votacion)

    def _pedir_siguiente_voto(
        self,
        ronda: Ronda,
        activos: List[Jugador],
        indice: int,
        al_finalizar_votacion: Callable[[Optional[Jugador]], None],
    ) -> None:
        if indice >= len(activos):
            acusado = self._contador_votos.contar_votos(ronda.votos)
            al_finalizar_votacion(acusado)
            return

        votante = activos[indice]
        candidatos = [j.nombre for j in activos]
        pistas_ronda = [(p.get_autor().nombre, p.get_texto()) for p in ronda.pistas]

        def procesar_voto(nombre_acusado: str) -> None:
            try:
                if not nombre_acusado:
                    raise VotoInvalidoException("Debes seleccionar un jugador para votar.")
                if nombre_acusado == votante.nombre:
                    raise VotoInvalidoException("No puedes votarte a ti mismo.")

                acusado_obj = next(
                    (j for j in activos if j.nombre == nombre_acusado), None
                )
                if acusado_obj is None:
                    raise VotoInvalidoException("El jugador seleccionado no es válido.")

                voto = votante.votar(acusado_obj)
                ronda.registrar_voto(voto)
                self._pedir_siguiente_voto(
                    ronda, activos, indice + 1, al_finalizar_votacion
                )
            except VotoInvalidoException as exc:
                self._vista.mostrar_error("Voto Inválido", str(exc))

        self._vista.mostrar_votacion_privada(
            numero_ronda=ronda.numero,
            nombre_votante=votante.nombre,
            candidatos=candidatos,
            pistas_ronda=pistas_ronda,
            on_registrar_voto=procesar_voto,
        )
