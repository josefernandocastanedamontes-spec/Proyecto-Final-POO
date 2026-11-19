from typing import Dict, Optional


class ResultadoPartida:
    def __init__(self, ganador: str, acusado=None, roles_revelados: Optional[Dict[str, str]] = None,
                 motivo: str = ""):
        self._ganador = ganador
        self._acusado = acusado
        self._roles_revelados = dict(roles_revelados or {})
        self._motivo = motivo

    @property
    def ganador(self) -> str:
        return self._ganador

    @property
    def acusado(self):
        return self._acusado

    @property
    def roles_revelados(self) -> Dict[str, str]:
        return dict(self._roles_revelados)

    @property
    def motivo(self) -> str:
        return self._motivo

    def generar_resumen(self) -> str:
        nombre_acusado = self._acusado.nombre if self._acusado else "Ninguno"
        detalle = f"Ganador: {self._ganador} | Acusado: {nombre_acusado}"
        return f"{detalle} | {self._motivo}" if self._motivo else detalle
