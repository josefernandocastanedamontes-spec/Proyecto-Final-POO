from modelos.categoria import Categoria

class PalabraSecreta:
    def __init__(self, texto: str, categoria: Categoria):
        self._texto = texto
        self._categoria = categoria

    def coincide_con(self, t: str) -> bool:
        return self._texto.lower() == t.strip().lower()

    @property
    def texto(self) -> str:
        return self._texto

    @property
    def categoria(self) -> Categoria:
        return self._categoria