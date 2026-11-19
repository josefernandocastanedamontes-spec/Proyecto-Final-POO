from modelos.categoria import Categoria


class ConfiguracionPartida:
    """Configuracion validada de una partida."""

    def __init__(self, numero_rondas: int, tiempo_debate: int, categoria: Categoria,
                 ultima_oportunidad: bool, longitud_max_pista: int):
        self._numero_rondas = numero_rondas
        self._tiempo_debate = tiempo_debate
        self._categoria = categoria
        self._ultima_oportunidad = ultima_oportunidad
        self._longitud_max_pista = longitud_max_pista

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
        if not isinstance(self._numero_rondas, int) or not 1 <= self._numero_rondas <= 10:
            raise ValueError("El numero de rondas debe estar entre 1 y 10.")
        if not isinstance(self._tiempo_debate, int) or not 10 <= self._tiempo_debate <= 300:
            raise ValueError("El tiempo de debate debe estar entre 10 y 300 segundos.")
        if not isinstance(self._categoria, Categoria):
            raise ValueError("Debes seleccionar una categoria valida.")
        if not isinstance(self._ultima_oportunidad, bool):
            raise ValueError("La ultima oportunidad debe ser verdadera o falsa.")
        if not isinstance(self._longitud_max_pista, int) or not 5 <= self._longitud_max_pista <= 60:
            raise ValueError("La longitud maxima de pista debe estar entre 5 y 60 caracteres.")
