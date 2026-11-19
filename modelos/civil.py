from modelos.rol import Rol
from modelos.palabrasecreta import PalabraSecreta


class Civil(Rol):
    def __init__(self, palabra_secreta: PalabraSecreta):
        super().__init__("Civil")
        self._palabra_secreta = palabra_secreta

    def conoce_palabra(self) -> bool:
        return True

    def obtener_palabra_visible(self) -> str:
        return (
            "¡ERES UN CIVIL!\n"
            "Descubre quién es el impostor.\n"
            f"Palabra secreta: {self._palabra_secreta.texto}"
        )

    def intentar_adivinar(self, texto: str, palabra_secreta=None) -> bool:
        return False
