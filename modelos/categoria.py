class Categoria:
    def __init__(self, nombre: str):
        self._nombre = nombre

    def obtener_nombre(self) -> str:
        return self._nombre