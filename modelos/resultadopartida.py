from typing import Dict
from modelos.jugador import Jugador

class ResultadoPartida:
    def __init__(self, ganador: str, acusado: Jugador, roles_revelados: Dict[str, str]):
        self._ganador = ganador
        self._acusado = acusado
        self._roles_revelados = roles_revelados

    def generar_resumen(self) -> str:
        nombre_acusado = self._acusado.nombre if self._acusado else "Ninguno"
        return f"Ganador: {self._ganador} | Acusado: {nombre_acusado}"