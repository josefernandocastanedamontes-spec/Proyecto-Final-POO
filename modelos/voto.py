class Voto:
    def __init__(self, votante, acusado):
        self._votante = votante
        self._acusado = acusado

    def get_acusado(self):
        return self._acusado
        
    @property
    def votante(self):
        return self._votante