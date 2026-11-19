from enum import Enum, auto


class EstadoJugador(Enum):
    ACTIVO = auto()
    ELIMINADO = auto()


class FaseJuego(Enum):
    REGISTRO = auto()
    ASIGNACION = auto()
    REVELACION = auto()
    PISTAS = auto()
    DEBATE = auto()
    VOTACION = auto()
    DESEMPATE = auto()
    RESULTADO = auto()
