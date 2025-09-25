"""
Estruturas fundamentais para o robô de salvamento
"""

from enum import Enum
from dataclasses import dataclass
from typing import Tuple


class Direcao(Enum):
    """Direções possíveis do robô (sentido horário)"""
    NORTE = 0  # ^
    LESTE = 1  # >
    SUL = 2    # v
    OESTE = 3  # <
    
    def girar_direita(self) -> 'Direcao':
        """Gira 90 graus à direita (sentido horário)"""
        return Direcao((self.value + 1) % 4)
    
    def get_delta(self) -> Tuple[int, int]:
        """Retorna a variação (dx, dy) para movimento nesta direção"""
        deltas = {
            Direcao.NORTE: (0, -1),
            Direcao.LESTE: (1, 0),
            Direcao.SUL: (0, 1),
            Direcao.OESTE: (-1, 0)
        }
        return deltas[self]


@dataclass
class Posicao:
    """Posição no labirinto"""
    x: int
    y: int
    
    def __add__(self, delta: Tuple[int, int]) -> 'Posicao':
        """Soma uma posição com um delta"""
        dx, dy = delta
        return Posicao(self.x + dx, self.y + dy)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Posicao):
            return False
        return self.x == other.x and self.y == other.y
    
    def __hash__(self) -> int:
        return hash((self.x, self.y))


class TipoSensor(Enum):
    """Tipos de leitura dos sensores"""
    PAREDE = "PAREDE"
    VAZIO = "VAZIO"
    HUMANO = "HUMANO"


class ComandoRobo(Enum):
    """Comandos disponíveis para o robô"""
    LIGAR = "LIGAR"
    AVANCAR = "A"
    GIRAR = "G"  # Gira 90 graus à direita
    PEGAR = "P"
    EJETAR = "E"


class StatusCarga(Enum):
    """Status do compartimento de carga"""
    SEM_CARGA = "SEM CARGA"
    COM_HUMANO = "COM HUMANO"


class TipoCelula(Enum):
    """Tipos de células no mapa"""
    PAREDE = "X"
    VAZIO = "."
    HUMANO = "@"
    ENTRADA = "E"


class RoboException(Exception):
    """Exceção base para erros do robô"""
    pass


class ColisaoException(RoboException):
    """ALARME: Tentativa de colisão com parede"""
    pass


class AtropelamentoException(RoboException):
    """ALARME: Tentativa de atropelamento de humano"""
    pass


class BecoSemSaidaException(RoboException):
    """ALARME: Robô com humano em beco sem saída"""
    pass


class OperacaoInvalidaException(RoboException):
    """ALARME: Operação inválida (pegar sem humano, ejetar sem humano, etc.)"""
    pass