from enum import Enum

class EstadoJugador(Enum):
    ACTIVO = 1
    ELIMINADO = 2

class FaseJuego(Enum):
    REGISTRO = 1
    ASIGNACION = 2
    PISTAS = 3
    DEBATE = 4
    VOTACION = 5
    RESULTADO = 6