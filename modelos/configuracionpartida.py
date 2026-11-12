from modelos.categoria import Categoria

class ConfiguracionPartida:
    def __init__(self, numero_rondas: int, tiempo_debate: int, categoria: Categoria, ultima_oportunidad: bool, longitud_max_pista: int):
        self._numero_rondas = numero_rondas
        self._tiempo_debate = tiempo_debate
        self._categoria = categoria
        self._ultima_oportunidad = ultima_oportunidad
        self._longitud_max_pista = longitud_max_pista

    def validar(self) -> None:
        if self._numero_rondas <= 0:
            raise ValueError("El número de rondas debe ser mayor a cero.")
        if self._longitud_max_pista <= 0:
            raise ValueError("La longitud máxima de pista debe ser válida.")