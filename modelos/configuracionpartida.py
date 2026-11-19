from modelos.categoria import Categoria
from modelos.excepciones import ConfiguracionInvalidaException


class ConfiguracionPartida:
    def __init__(
        self,
        numero_rondas: int,
        tiempo_debate: int,
        categoria: Categoria,
        ultima_oportunidad: bool,
        longitud_max_pista: int,
    ):
        self._numero_rondas = numero_rondas
        self._tiempo_debate = tiempo_debate
        self._categoria = categoria
        self._ultima_oportunidad = bool(ultima_oportunidad)
        self._longitud_max_pista = longitud_max_pista
        self.validar()

    @property
    def numero_rondas(self) -> int:
        return self._numero_rondas

    @property
    def tiempo_debate(self) -> int:
        return self._tiempo_debate

    @property
    def categoria(self) -> Categoria:
        return self._categoria

    @property
    def ultima_oportunidad(self) -> bool:
        return self._ultima_oportunidad

    @property
    def longitud_max_pista(self) -> int:
        return self._longitud_max_pista

    def validar(self) -> None:
        if not isinstance(self._numero_rondas, int) or self._numero_rondas < 1:
            raise ConfiguracionInvalidaException("El número de rondas debe ser un entero mayor que cero.")
        if not isinstance(self._tiempo_debate, int) or self._tiempo_debate < 0:
            raise ConfiguracionInvalidaException("El tiempo de debate no puede ser negativo.")
        if not isinstance(self._categoria, Categoria):
            raise ConfiguracionInvalidaException("Debes seleccionar una categoría válida.")
        if not isinstance(self._longitud_max_pista, int) or self._longitud_max_pista < 1:
            raise ConfiguracionInvalidaException("La longitud máxima de la pista debe ser mayor que cero.")
