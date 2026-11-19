from typing import Dict, Optional
from modelos.jugador import Jugador


class ResultadoPartida:
    def __init__(self, ganador: str, acusado: Optional[Jugador], roles_revelados: Dict[str, str]):
        self._ganador = ganador
        self._acusado = acusado
        self._roles_revelados = dict(roles_revelados)

    @property
    def ganador(self) -> str:
        return self._ganador

    @property
    def acusado(self) -> Optional[Jugador]:
        return self._acusado

    @property
    def roles_revelados(self) -> Dict[str, str]:
        return dict(self._roles_revelados)

    def generar_resumen(self) -> str:
        nombre_acusado = self._acusado.nombre if self._acusado else "Ninguno"
        return f"Ganador: {self._ganador} | Acusado: {nombre_acusado}"
