class Pista:
    def __init__(self, autor, texto: str, numero_turno: int):
        if not isinstance(texto, str):
            raise TypeError("La pista debe ser texto.")
        self._autor = autor
        self._texto = texto.strip()
        self._numero_turno = numero_turno

    def get_texto(self) -> str:
        return self._texto

    def get_autor(self):
        return self._autor

    @property
    def texto(self) -> str:
        return self._texto

    @property
    def autor(self):
        return self._autor

    @property
    def numero_turno(self) -> int:
        return self._numero_turno
