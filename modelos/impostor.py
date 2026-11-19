from typing import Optional

from modelos.rol import Rol
from modelos.palabrasecreta import PalabraSecreta


class Impostor(Rol):
    def __init__(self):
        super().__init__("Impostor")
        self._intento_disponible = True

    @property
    def intento_disponible(self) -> bool:
        return self._intento_disponible

    def conoce_palabra(self) -> bool:
        return False

    def obtener_palabra_visible(self) -> str:
        return "¡ERES EL IMPOSTOR!\nDisimula y averigua la palabra.\nNo conoces la palabra secreta."

    def intentar_adivinar(self, texto: str, palabra_secreta: Optional[PalabraSecreta] = None) -> bool:
        if not self._intento_disponible:
            return False
        self._intento_disponible = False
        if palabra_secreta is None:
            return False
        return palabra_secreta.coincide_con(texto)
