class Categoria:
    def __init__(self, nombre: str):
        nombre_limpio = nombre.strip() if isinstance(nombre, str) else ""
        if not nombre_limpio:
            raise ValueError("El nombre de la categoría es obligatorio.")
        self._nombre = nombre_limpio

    def obtener_nombre(self) -> str:
        return self._nombre

    def __str__(self) -> str:
        return self._nombre

    def __eq__(self, other) -> bool:
        return isinstance(other, Categoria) and self._nombre.casefold() == other._nombre.casefold()

    def __hash__(self) -> int:
        return hash(self._nombre.casefold())
