# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Callable, Dict, List


class IVistaRegistro(ABC):
    @abstractmethod
    def mostrar_registro(
        self,
        categorias: List[str],
        jugadores_actuales: List[str],
        on_agregar_jugador: Callable[[str], None],
        on_eliminar_jugador: Callable[[int], None],
        on_iniciar_partida: Callable[[str, int, int, int, bool], None],
    ) -> None:
        pass


class IVistaTurno(ABC):
    @abstractmethod
    def mostrar_asignacion_privada(
        self,
        nombre_jugador: str,
        numero_jugador: int,
        total_jugadores: int,
        obtener_texto_rol: Callable[[], str],
        on_siguiente_jugador: Callable[[], None],
    ) -> None:
        pass

    @abstractmethod
    def mostrar_turno_pista(
        self,
        numero_ronda: int,
        categoria: str,
        nombre_jugador: str,
        pistas_previas: List[tuple],
        longitud_maxima: int,
        on_enviar_pista: Callable[[str], None],
    ) -> None:
        pass

    @abstractmethod
    def mostrar_debate(
        self,
        numero_ronda: int,
        categoria: str,
        pistas_ronda: List[tuple],
        segundos_debate: int,
        on_finalizar_debate: Callable[[], None],
    ) -> None:
        pass


class IVistaVotacion(ABC):
    @abstractmethod
    def mostrar_votacion_privada(
        self,
        numero_ronda: int,
        nombre_votante: str,
        candidatos: List[str],
        pistas_ronda: List[tuple],
        on_registrar_voto: Callable[[str], None],
    ) -> None:
        pass

    @abstractmethod
    def solicitar_ultima_oportunidad(
        self,
        nombre_impostor: str,
        on_adivinar_palabra: Callable[[str], None],
    ) -> None:
        pass


class IVistaResultado(ABC):
    @abstractmethod
    def mostrar_resultado_final(
        self,
        ganador: str,
        detalle: str,
        palabra_secreta: str,
        roles_revelados: List[tuple],
        marcador_acumulado: Dict[str, int],
        on_nueva_partida: Callable[[], None],
        on_volver_registro: Callable[[], None],
    ) -> None:
        pass


class IVistaJuego(IVistaRegistro, IVistaTurno, IVistaVotacion, IVistaResultado, ABC):
    @abstractmethod
    def mostrar_error(self, titulo: str, mensaje: str) -> None:
        pass

    @abstractmethod
    def mostrar_info(self, titulo: str, mensaje: str) -> None:
        pass

    @abstractmethod
    def iniciar(self) -> None:
        pass
