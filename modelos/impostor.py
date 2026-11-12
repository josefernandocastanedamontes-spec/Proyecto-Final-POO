from modelos.rol import Rol

class Impostor(Rol):
    def __init__(self):
        super().__init__("Impostor")
        self._intento_disponible = True

    def conoce_palabra(self) -> bool:
        return False

    def obtener_palabra_visible(self) -> str:
        return ("¡ERES EL IMPOSTOR!\n"
                "Disimula y averigua la palabra.\n"
                "Palabra secreta: ???")

    def intentar_adivinar(self, t: str) -> bool:
        if self._intento_disponible:
            self._intento_disponible = False
            return True 
        return False