from typing import List, Optional

from modelos.enumeraciones import FaseJuego
from modelos.pista import Pista
from modelos.voto import Voto
from modelos.excepciones import FaseInvalidaException, PistaInvalidaException, VotoInvalidoException


class Ronda:
    def __init__(self, numero: int):
        self._numero = numero
        self._pistas: List[Pista] = []
        self._votos: List[Voto] = []
        self._fase = FaseJuego.ASIGNACION
        self._votantes_desempate = set()
        self._votos_desempate: List[Voto] = []
        self._candidatos_desempate = []
        self._acusado = None

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def pistas(self) -> List[Pista]:
        return list(self._pistas)

    @property
    def votos(self) -> List[Voto]:
        return list(self._votos)

    @property
    def fase(self) -> FaseJuego:
        return self._fase

    @property
    def votos_desempate(self) -> List[Voto]:
        return list(self._votos_desempate)

    @property
    def candidatos_desempate(self):
        return list(self._candidatos_desempate)

    @property
    def acusado(self):
        return self._acusado

    def avanzar_fase(self, nueva_fase: Optional[FaseJuego] = None) -> FaseJuego:
        transiciones = {
            FaseJuego.ASIGNACION: FaseJuego.REVELACION,
            FaseJuego.REVELACION: FaseJuego.PISTAS,
            FaseJuego.PISTAS: FaseJuego.DEBATE,
            FaseJuego.DEBATE: FaseJuego.VOTACION,
            FaseJuego.VOTACION: FaseJuego.RESULTADO,
            FaseJuego.DESEMPATE: FaseJuego.RESULTADO,
        }
        esperada = transiciones.get(self._fase)
        if nueva_fase is not None:
            permitidas = {esperada}
            if self._fase is FaseJuego.VOTACION:
                permitidas.add(FaseJuego.DESEMPATE)
            if nueva_fase not in permitidas:
                raise FaseInvalidaException(f"No se puede pasar de {self._fase.name} a {nueva_fase.name}.")
            self._fase = nueva_fase
        elif esperada is not None:
            self._fase = esperada
        else:
            raise FaseInvalidaException("La ronda ya está en su fase final.")
        return self._fase

    def registrar_pista(self, pista: Pista) -> None:
        if self._fase is not FaseJuego.PISTAS:
            raise FaseInvalidaException("Solo se pueden registrar pistas durante la fase de pistas.")
        if not isinstance(pista, Pista) or pista.autor is None or not pista.texto:
            raise PistaInvalidaException("La pista o su autor no son válidos.")
        if any(p.autor is pista.autor for p in self._pistas):
            raise PistaInvalidaException("Este jugador ya registró una pista en esta ronda.")
        self._pistas.append(pista)

    def registrar_voto(self, voto: Voto) -> None:
        if self._fase is not FaseJuego.VOTACION:
            raise FaseInvalidaException("No es el momento de votar.")
        if not isinstance(voto, Voto):
            raise VotoInvalidoException("El voto no es válido.")
        if any(v.votante is voto.votante for v in self._votos):
            raise VotoInvalidoException("Este jugador ya votó.")
        if voto.votante is voto.acusado:
            raise VotoInvalidoException("No puedes votar por ti mismo.")
        self._votos.append(voto)

    def iniciar_desempate(self, candidatos) -> None:
        if self._fase is not FaseJuego.VOTACION:
            raise FaseInvalidaException("El desempate solo puede iniciar después de la votación inicial.")
        candidatos = list(candidatos)
        if len(candidatos) < 2:
            raise ValueError("El desempate requiere al menos dos candidatos.")
        self._candidatos_desempate = candidatos
        self._votos_desempate.clear()
        self._votantes_desempate.clear()
        self._fase = FaseJuego.DESEMPATE

    def registrar_voto_desempate(self, voto: Voto) -> None:
        if self._fase is not FaseJuego.DESEMPATE:
            raise FaseInvalidaException("La ronda no está en desempate.")
        if voto.votante in self._votantes_desempate:
            raise VotoInvalidoException("Este jugador ya votó en el desempate.")
        if voto.acusado not in self._candidatos_desempate:
            raise VotoInvalidoException("En el desempate solo puedes votar por los jugadores empatados.")
        if voto.votante is voto.acusado:
            raise VotoInvalidoException("No puedes votar por ti mismo.")
        self._votos_desempate.append(voto)
        self._votantes_desempate.add(voto.votante)

    def establecer_acusado(self, jugador) -> None:
        if self._fase not in (FaseJuego.VOTACION, FaseJuego.DESEMPATE):
            raise FaseInvalidaException("No se puede establecer un acusado en esta fase.")
        self._acusado = jugador
