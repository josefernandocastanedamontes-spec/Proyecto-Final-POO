from modelos.categoria import Categoria


class PalabraSecreta:
    def __init__(self, texto: str, categoria: Categoria):
        texto_limpio = texto.strip() if isinstance(texto, str) else ""
        if not texto_limpio:
            raise ValueError("La palabra secreta no puede estar vacía.")
        if not isinstance(categoria, Categoria):
            raise TypeError("La palabra debe pertenecer a una categoría válida.")
        self._texto = texto_limpio
        self._categoria = categoria

    def coincide_con(self, texto: str) -> bool:
        return self.normalizar(texto) == self.normalizar(self._texto)

    @staticmethod
    def normalizar(texto: str) -> str:
        return " ".join((texto or "").casefold().split())

    @property
    def texto(self) -> str:
        return self._texto

    @property
    def categoria(self) -> Categoria:
        return self._categoria
