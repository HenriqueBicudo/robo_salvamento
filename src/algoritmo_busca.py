"""
Algoritmo inteligente de busca e salvamento
Implementa busca autônoma baseada apenas em sensores
Autor: [SEU NOME E MATRÍCULA AQUI]
"""

from typing import Dict, Set, List, Optional, Tuple
from collections import deque
from .estruturas import (
    Posicao, Direcao, ComandoRobo, TipoSensor,
    RoboException
)
from .robo import Robo


class AlgoritmoBusca:
    """Algoritmo inteligente para busca e salvamento autônomo"""
    
    def __init__(self, robo: Robo):
        """Inicializa o algoritmo com o robô"""
        self.robo = robo
        
        # Mapa interno construído pelos sensores
        self.mapa_conhecido: Dict[Posicao, TipoSensor] = {}
        self.visitadas: Set[Posicao] = set()
        self.caminho_percorrido: List[Tuple[Posicao, Direcao]] = []
        
        # Estados da missão
        self.humano_encontrado = False
        self.humano_coletado = False
        self.missao_concluida = False
        
        # Registra posição inicial
        self._atualizar_mapa()
        self.posicao_entrada = self.robo.posicao
    
    def _atualizar_mapa(self) -> None:
        """Atualiza o mapa interno com leituras dos sensores"""
        posicao_atual = self.robo.posicao
        
        # Registra posições detectadas pelos sensores
        self._registrar_sensor_esquerdo()
        self._registrar_sensor_direito()
        self._registrar_sensor_frente()
        
        # Marca posição atual como visitada
        self.visitadas.add(posicao_atual)
        self.mapa_conhecido[posicao_atual] = TipoSensor.VAZIO
    
    def _registrar_sensor_esquerdo(self) -> None:
        """Registra leitura do sensor esquerdo no mapa"""
        direcao_esquerda = Direcao((self.robo.direcao.value - 1) % 4)
        posicao_esquerda = self.robo.posicao + direcao_esquerda.get_delta()
        leitura = self.robo._ler_sensor_esquerdo()
        self.mapa_conhecido[posicao_esquerda] = leitura
    
    def _registrar_sensor_direito(self) -> None:
        """Registra leitura do sensor direito no mapa"""
        direcao_direita = self.robo.direcao.girar_direita()
        posicao_direita = self.robo.posicao + direcao_direita.get_delta()
        leitura = self.robo._ler_sensor_direito()
        self.mapa_conhecido[posicao_direita] = leitura
    
    def _registrar_sensor_frente(self) -> None:
        """Registra leitura do sensor da frente no mapa"""
        posicao_frente = self.robo.posicao + self.robo.direcao.get_delta()
        leitura = self.robo._ler_sensor_frente()
        self.mapa_conhecido[posicao_frente] = leitura
    
    def _pode_mover_para(self, posicao: Posicao) -> bool:
        """Verifica se pode mover para uma posição baseado no mapa conhecido"""
        if posicao not in self.mapa_conhecido:
            return False  # Posição desconhecida
        
        tipo = self.mapa_conhecido[posicao]
        return tipo == TipoSensor.VAZIO or tipo == TipoSensor.HUMANO
    
    def _escolher_proxima_direcao(self) -> Optional[Direcao]:
        """Escolhe a próxima direção usando estratégia de exploração"""
        posicao_atual = self.robo.posicao
        
        # Lista todas as direções possíveis em ordem de prioridade
        # (primeiro tenta manter direção atual, depois esquerda, direita, trás)
        direcoes = [
            self.robo.direcao,  # Frente
            Direcao((self.robo.direcao.value - 1) % 4),  # Esquerda
            self.robo.direcao.girar_direita(),  # Direita
            Direcao((self.robo.direcao.value + 2) % 4)   # Trás
        ]
        
        for direcao in direcoes:
            nova_posicao = posicao_atual + direcao.get_delta()
            
            # Prioriza posições não visitadas
            if (self._pode_mover_para(nova_posicao) and 
                nova_posicao not in self.visitadas):
                return direcao
        
        # Se não há posições não visitadas, pode revisitar
        for direcao in direcoes:
            nova_posicao = posicao_atual + direcao.get_delta()
            
            if self._pode_mover_para(nova_posicao):
                return direcao
        
        return None  # Nenhuma direção válida
    
    def _virar_para_direcao(self, direcao_alvo: Direcao) -> None:
        """Vira o robô para a direção especificada"""
        while self.robo.direcao != direcao_alvo:
            self.robo.girar()
            self._atualizar_mapa()
    
    def _explorar_ate_encontrar_humano(self) -> None:
        """Explora o labirinto até encontrar o humano"""
        max_iteracoes = 10000  # Proteção contra loops infinitos
        iteracao = 0
        
        while not self.humano_encontrado and iteracao < max_iteracoes:
            iteracao += 1
            
            # Atualiza mapa com sensores atuais
            self._atualizar_mapa()
            
            # Verifica se humano está à frente
            if self.robo._ler_sensor_frente() == TipoSensor.HUMANO:
                self.humano_encontrado = True
                return
            
            # Escolhe próxima direção
            proxima_direcao = self._escolher_proxima_direcao()
            
            if proxima_direcao is None:
                raise RoboException("Robô ficou preso - nenhuma direção válida!")
            
            # Vira para a direção escolhida se necessário
            self._virar_para_direcao(proxima_direcao)
            
            # Move para frente
            self.robo.avancar()
            
            # Registra movimento no caminho
            self.caminho_percorrido.append((self.robo.posicao, self.robo.direcao))
        
        if not self.humano_encontrado:
            raise RoboException("Limite de iterações atingido sem encontrar humano!")
    
    def _calcular_caminho_volta(self) -> List[Posicao]:
        """Calcula caminho eficiente de volta à entrada EVITANDO becos sem saída"""
        # BFS para encontrar caminho mais curto conhecido QUE EVITA BECOS
        fila = deque([(self.robo.posicao, [])])
        visitados_bfs = {self.robo.posicao}
        
        while fila:
            posicao_atual, caminho = fila.popleft()
            
            # Se chegou à entrada, retorna caminho
            if posicao_atual == self.posicao_entrada:
                return caminho + [posicao_atual]
            
            # Explora vizinhos conhecidos
            for direcao in Direcao:
                nova_posicao = posicao_atual + direcao.get_delta()
                
                if (nova_posicao not in visitados_bfs and
                    nova_posicao in self.mapa_conhecido and
                    self.mapa_conhecido[nova_posicao] == TipoSensor.VAZIO):
                    
                    # VALIDAÇÃO CRÍTICA: Evita becos sem saída com humano
                    if self._e_beco_sem_saida(nova_posicao):
                        continue  # Pula posições que são becos sem saída
                    
                    visitados_bfs.add(nova_posicao)
                    novo_caminho = caminho + [posicao_atual]
                    fila.append((nova_posicao, novo_caminho))
        
        raise RoboException("Não foi possível encontrar caminho de volta!")
    
    def _e_beco_sem_saida(self, posicao: Posicao) -> bool:
        """Verifica se uma posição é um beco sem saída"""
        if posicao == self.posicao_entrada:
            return False  # Entrada nunca é beco sem saída
        
        # Conta quantas saídas a posição tem
        saidas = 0
        for direcao in Direcao:
            posicao_vizinha = posicao + direcao.get_delta()
            
            # Se conhece a posição e não é parede, conta como saída
            if (posicao_vizinha in self.mapa_conhecido and 
                self.mapa_conhecido[posicao_vizinha] != TipoSensor.PAREDE):
                saidas += 1
        
        # Se tem apenas 1 saída ou menos, é beco sem saída
        return saidas <= 1
    
    def _mover_para_posicao(self, posicao_alvo: Posicao) -> None:
        """Move o robô para uma posição específica"""
        posicao_atual = self.robo.posicao
        
        # Calcula direção necessária
        dx = posicao_alvo.x - posicao_atual.x
        dy = posicao_alvo.y - posicao_atual.y
        
        # Determina direção baseada no delta
        if dx > 0:
            direcao_alvo = Direcao.LESTE
        elif dx < 0:
            direcao_alvo = Direcao.OESTE
        elif dy > 0:
            direcao_alvo = Direcao.SUL
        elif dy < 0:
            direcao_alvo = Direcao.NORTE
        else:
            return  # Já está na posição
        
        # Vira para a direção e move
        self._virar_para_direcao(direcao_alvo)
        self.robo.avancar()
        self._atualizar_mapa()
    
    def _voltar_para_entrada(self) -> None:
        """Retorna à entrada pelo caminho mais eficiente"""
        caminho_volta = self._calcular_caminho_volta()
        
        for posicao_alvo in caminho_volta:
            if self.robo.posicao != posicao_alvo:
                self._mover_para_posicao(posicao_alvo)
    
    def executar_missao(self) -> bool:
        """Executa a missão completa de busca e salvamento"""
        try:
            print("🤖 Iniciando missão de busca e salvamento...")
            
            # Fase 1: Explorar até encontrar humano
            print("📍 Fase 1: Explorando labirinto...")
            self._explorar_ate_encontrar_humano()
            print("✅ Humano encontrado!")
            
            # Fase 2: Coletar humano
            print("🔄 Fase 2: Coletando humano...")
            self.robo.pegar_humano()
            self.humano_coletado = True
            print("✅ Humano coletado!")
            
            # Fase 3: Retornar à entrada
            print("🏠 Fase 3: Retornando à entrada...")
            self._voltar_para_entrada()
            print("✅ Chegou à entrada!")
            
            # Fase 4: Ejetar humano
            print("🚀 Fase 4: Ejetando humano...")
            self.robo.ejetar_humano()
            self.missao_concluida = True
            print("✅ Missão concluída com sucesso!")
            
            return True
            
        except Exception as e:
            print(f"❌ Falha na missão: {e}")
            return False
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas da exploração"""
        return {
            'posicoes_visitadas': len(self.visitadas),
            'posicoes_conhecidas': len(self.mapa_conhecido),
            'caminho_percorrido': len(self.caminho_percorrido),
            'humano_encontrado': self.humano_encontrado,
            'humano_coletado': self.humano_coletado,
            'missao_concluida': self.missao_concluida
        }