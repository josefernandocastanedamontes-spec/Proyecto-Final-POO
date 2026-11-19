# -*- coding: utf-8 -*-
from typing import Callable, List, Optional
from modelos.enumeraciones import EstadoJugador
from modelos.excepciones import VotoInvalidoException
from modelos.jugador import Jugador
from modelos.ronda import Ronda
from servicios.conteo import IContadorVotos
from vista.interfaces import IVistaJuego


class ControladorVotacion:
    """Coordina la votacion inicial y una eventual segunda votacion de desempate."""

    def __init__(self, vista: IVistaJuego, contador_votos: IContadorVotos):
        self._vista = vista
        self._contador_votos = contador_votos

    def iniciar_votacion(
        self,
        ronda: Ronda,
        jugadores_ordenados: List[Jugador],
        al_finalizar_votacion: Callable[[Optional[Jugador]], None],
    ) -> None:
        ronda.avanzar_fase()
        activos = [j for j in jugadores_ordenados if j.estado == EstadoJugador.ACTIVO]
        self._pedir_siguiente_voto(
            ronda, activos, 0, al_finalizar_votacion,
            candidatos_permitidos=None, es_desempate=False,
        )

    def _pedir_siguiente_voto(
        self,
        ronda: Ronda,
        activos: List[Jugador],
        indice: int,
        al_finalizar_votacion: Callable[[Optional[Jugador]], None],
        candidatos_permitidos: Optional[List[Jugador]],
        es_desempate: bool,
    ) -> None:
        if indice >= len(activos):
            votos = ronda.votos_desempate if es_desempate else ronda.votos
            acusado = self._contador_votos.contar_votos(votos)
            if not es_desempate:
                empatados = self._contador_votos.obtener_candidatos_empatados(votos)
                if len(empatados) > 1:
                    self._vista.mostrar_info(
                        "Empate en la votacion",
                        "Se realizara una segunda votacion entre los jugadores empatados.",
                    )
                    self._pedir_siguiente_voto(
                        ronda, activos, 0, al_finalizar_votacion,
                        candidatos_permitidos=empatados, es_desempate=True,
                    )
                    return
            al_finalizar_votacion(acusado)
            return

        votante = activos[indice]
        universo = candidatos_permitidos if candidatos_permitidos is not None else activos
        candidatos = [j for j in universo if j is not votante]
        pistas_ronda = [(p.get_autor().nombre, p.get_texto()) for p in ronda.pistas]

        def procesar_voto(nombre_acusado: str) -> None:
            try:
                if not nombre_acusado:
                    raise VotoInvalidoException("Debes seleccionar un jugador para votar.")
                acusado_obj = next((j for j in candidatos if j.nombre == nombre_acusado), None)
                if acusado_obj is None:
                    raise VotoInvalidoException(
                        "El jugador seleccionado no es un candidato valido para esta votacion."
                    )
                voto = votante.votar(acusado_obj)
                ronda.registrar_voto(voto, desempate=es_desempate)
                self._pedir_siguiente_voto(
                    ronda, activos, indice + 1, al_finalizar_votacion,
                    candidatos_permitidos, es_desempate,
                )
            except (VotoInvalidoException, ValueError) as exc:
                self._vista.mostrar_error("Voto invalido", str(exc))

        self._vista.mostrar_votacion_privada(
            numero_ronda=ronda.numero,
            nombre_votante=votante.nombre,
            candidatos=[j.nombre for j in candidatos],
            pistas_ronda=pistas_ronda,
            on_registrar_voto=procesar_voto,
        )
