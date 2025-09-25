"""
Simulador do ambiente virtual do robô de salvamento
Responsável por carregar e simular o labirinto
"""

from typing import List, Optional
from .estruturas import (
    Posicao, Direcao, TipoCelula, TipoSensor,
    RoboException
)


class Labirinto:
    """Simulador do ambiente virtual do labirinto"""
    
    def __init__(self, arquivo_mapa: str):
        """Inicializa o labirinto a partir de um arquivo"""
        self.mapa: List[List[str]] = []
        self.largura: int = 0
        self.altura: int = 0
        self.entrada: Optional[Posicao] = None
        self.posicao_humano: Optional[Posicao] = None
        self.humano_coletado: bool = False
        
        self._carregar_mapa(arquivo_mapa)
        self._encontrar_entrada_e_humano()
    
    def _carregar_mapa(self, arquivo_mapa: str) -> None:
        """Carrega o mapa a partir do arquivo"""
        try:
            with open(arquivo_mapa, 'r', encoding='utf-8') as arquivo:
                linhas = arquivo.read().strip().split('\n')
                
            if not linhas:
                raise RoboException("Arquivo de mapa vazio")
            
            self.altura = len(linhas)
            self.largura = len(linhas[0]) if linhas else 0
            
            # Valida se todas as linhas têm o mesmo tamanho
            for i, linha in enumerate(linhas):
                if len(linha) != self.largura:
                    raise RoboException(f"Linha {i+1} tem tamanho diferente das demais")
            
            self.mapa = [list(linha) for linha in linhas]
            
        except FileNotFoundError:
            raise RoboException(f"Arquivo não encontrado: {arquivo_mapa}")
        except Exception as e:
            raise RoboException(f"Erro ao carregar mapa: {e}")
    
    def _encontrar_entrada_e_humano(self) -> None:
        """Encontra a entrada e a posição inicial do humano"""
        entrada_encontrada = False
        humano_encontrado = False
        
        for y in range(self.altura):
            for x in range(self.largura):
                celula = self.mapa[y][x]
                
                if celula == TipoCelula.ENTRADA.value:
                    if entrada_encontrada:
                        raise RoboException("Múltiplas entradas encontradas no mapa")
                    
                    # Valida se a entrada está na borda
                    if not (x == 0 or x == self.largura-1 or y == 0 or y == self.altura-1):
                        raise RoboException("Entrada deve estar na borda do labirinto")
                    
                    self.entrada = Posicao(x, y)
                    entrada_encontrada = True
                
                elif celula == TipoCelula.HUMANO.value:
                    if humano_encontrado:
                        raise RoboException("Múltiplos humanos encontrados no mapa")
                    
                    self.posicao_humano = Posicao(x, y)
                    humano_encontrado = True
        
        if not entrada_encontrada:
            raise RoboException("Nenhuma entrada encontrada no mapa")
        
        if not humano_encontrado:
            raise RoboException("Nenhum humano encontrado no mapa")
    
    def posicao_valida(self, posicao: Posicao) -> bool:
        """Verifica se uma posição está dentro dos limites do mapa"""
        return (0 <= posicao.x < self.largura and 
                0 <= posicao.y < self.altura)
    
    def get_tipo_celula(self, posicao: Posicao) -> TipoCelula:
        """Retorna o tipo da célula na posição especificada"""
        if not self.posicao_valida(posicao):
            return TipoCelula.PAREDE  # Fora do mapa é considerado parede
        
        celula = self.mapa[posicao.y][posicao.x]
        
        # Se o humano foi coletado, a posição dele vira espaço vazio
        if (celula == TipoCelula.HUMANO.value and 
            self.humano_coletado and 
            posicao == self.posicao_humano):
            return TipoCelula.VAZIO
        
        # Converte caractere para enum
        for tipo in TipoCelula:
            if tipo.value == celula:
                return tipo
        
        # Se não reconhecer, considera parede por segurança
        return TipoCelula.PAREDE
    
    def ler_sensor(self, posicao: Posicao) -> TipoSensor:
        """Simula a leitura de um sensor na posição especificada"""
        tipo_celula = self.get_tipo_celula(posicao)
        
        if tipo_celula == TipoCelula.PAREDE:
            return TipoSensor.PAREDE
        elif (tipo_celula == TipoCelula.HUMANO and 
              not self.humano_coletado):
            return TipoSensor.HUMANO
        else:
            # VAZIO, ENTRADA ou HUMANO já coletado
            return TipoSensor.VAZIO
    
    def pode_mover_para(self, posicao: Posicao) -> bool:
        """Verifica se o robô pode se mover para a posição"""
        tipo_celula = self.get_tipo_celula(posicao)
        
        # Não pode mover para paredes
        if tipo_celula == TipoCelula.PAREDE:
            return False
        
        # Não pode atropelar humano
        if (tipo_celula == TipoCelula.HUMANO and 
            not self.humano_coletado):
            return False
        
        return True
    
    def coletar_humano(self, posicao_robo: Posicao) -> bool:
        """Tenta coletar o humano (deve estar exatamente na posição especificada)"""
        if self.humano_coletado:
            return False
        
        # Verifica se a posição do robô é exatamente onde está o humano
        if posicao_robo == self.posicao_humano:
            self.humano_coletado = True
            return True
        
        return False
    
    def ejetar_humano(self) -> bool:
        """Ejeta o humano (deve estar na entrada)"""
        if not self.humano_coletado:
            return False
        
        self.humano_coletado = False
        return True
    
    def get_direcao_inicial(self) -> Direcao:
        """Determina a direção inicial do robô baseada na posição da entrada"""
        if not self.entrada:
            raise RoboException("Entrada não encontrada")
        
        x, y = self.entrada.x, self.entrada.y
        
        # Entrada na borda superior - robô olha para baixo
        if y == 0:
            return Direcao.SUL
        # Entrada na borda inferior - robô olha para cima
        elif y == self.altura - 1:
            return Direcao.NORTE
        # Entrada na borda esquerda - robô olha para direita
        elif x == 0:
            return Direcao.LESTE
        # Entrada na borda direita - robô olha para esquerda
        elif x == self.largura - 1:
            return Direcao.OESTE
        else:
            raise RoboException("Entrada não está na borda do labirinto")
    
    def __str__(self) -> str:
        """Representação em string do labirinto"""
        resultado = []
        for linha in self.mapa:
            resultado.append(''.join(linha))
        return '\n'.join(resultado)