class JuegoException(Exception):
    """Excepción base para errores controlados del juego."""


class PistaInvalidaException(JuegoException):
    pass


class VotoInvalidoException(JuegoException):
    pass


class FaseInvalidaException(JuegoException):
    pass


class RegistroJugadorException(JuegoException):
    pass


class BancoPalabrasVacioException(JuegoException):
    pass


class ConfiguracionInvalidaException(JuegoException):
    pass
