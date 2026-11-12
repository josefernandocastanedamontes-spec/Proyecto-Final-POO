from modelos.rol import Rol
from modelos.palabrasecreta import PalabraSecreta

class Civil(Rol):
    def __init__(self, palabra_secreta: PalabraSecreta):
        super().__init__("Civil")
        self._palabra_secreta = palabra_secreta

    def conoce_palabra(self) -> bool:
        return True

    def obtener_palabra_visible(self) -> str:
        return (f"¡ERES UN CIVIL!\n"
                f"Descubre quién miente.\n"
                f"Palabra secreta: {self._palabra_secreta.texto}")

    def intentar_adivinar(self, t: str) -> bool:
        return False