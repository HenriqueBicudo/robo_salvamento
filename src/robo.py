"""
Hardware embarcado do robô de salvamento
Implementa sensores, atuadores e validações de segurança
Autor: [SEU NOME E MATRÍCULA AQUI]
"""

from typing import Dict, Set, Optional
from .estruturas import (
    Posicao, Direcao, ComandoRobo, TipoSensor, StatusCarga,
    ColisaoException, AtropelamentoException, BecoSemSaidaException,
    OperacaoInvalidaException
)
from .labirinto import Labirinto
from .logger import LoggerRobo


class Robo:
    """Hardware embarcado do robô com sensores, atuadores e validações"""
    
    def __init__(self, labirinto: Labirinto, logger: LoggerRobo):
        """Inicializa o robô no labirinto"""
        self.labirinto = labirinto
        self.logger = logger
        
        # Estado do robô
        self.posicao = labirinto.entrada
        self.direcao = labirinto.get_direcao_inicial()
        self.tem_humano = False
        self.direcao_interior = self.direcao
        self.direcao_saida = Direcao((self.direcao.value + 2) % 4)
        
        # Registro inicial dos sensores ao ligar
        self._registrar_leitura_inicial()
    
    def _registrar_leitura_inicial(self) -> None:
        """Registra a leitura inicial dos sensores ao ligar o robô"""
        sensor_esquerdo = self._ler_sensor_esquerdo()
        sensor_direito = self._ler_sensor_direito()
        sensor_frente = self._ler_sensor_frente()
        status_carga = StatusCarga.SEM_CARGA
        
        self.logger.registrar_operacao(
            ComandoRobo.LIGAR,
            sensor_esquerdo,
            sensor_direito,
            sensor_frente,
            status_carga
        )
    
    def _ler_sensor_na_direcao(self, direcao_sensor: Direcao) -> TipoSensor:
        """Lê um sensor apontado para uma direção absoluta específica"""
        # Ao chegar na entrada, considere a saída como espaço livre para evitar claustrofobia
        if self._esta_na_entrada() and direcao_sensor == self.direcao_saida:
            return TipoSensor.VAZIO

        posicao_sensor = self.posicao + direcao_sensor.get_delta()
        return self.labirinto.ler_sensor(posicao_sensor)

    def _ler_sensor_esquerdo(self) -> TipoSensor:
        """Lê o sensor do lado esquerdo do robô"""
        # Calcula direção à esquerda (3 posições no sentido anti-horário)
        direcao_esquerda = Direcao((self.direcao.value - 1) % 4)
        return self._ler_sensor_na_direcao(direcao_esquerda)
    
    def _ler_sensor_direito(self) -> TipoSensor:
        """Lê o sensor do lado direito do robô"""
        direcao_direita = self.direcao.girar_direita()
        return self._ler_sensor_na_direcao(direcao_direita)
    
    def _ler_sensor_frente(self) -> TipoSensor:
        """Lê o sensor da frente do robô"""
        return self._ler_sensor_na_direcao(self.direcao)
    
    def _get_status_carga(self) -> StatusCarga:
        """Retorna o status atual do compartimento de carga"""
        return StatusCarga.COM_HUMANO if self.tem_humano else StatusCarga.SEM_CARGA
    
    def _esta_na_entrada(self, posicao: Optional[Posicao] = None) -> bool:
        """Verifica se uma posição corresponde à entrada do labirinto"""
        posicao_checar = posicao if posicao is not None else self.posicao
        return self.labirinto.entrada == posicao_checar

    def _ajustar_orientacao_para_interior(self) -> None:
        """Garante que o robô esteja virado para dentro ao chegar na entrada"""
        if self.direcao != self.direcao_interior:
            self.direcao = self.direcao_interior

    def _girar_para_direcao(self, direcao_alvo: Direcao) -> None:
        """Gira o robô até ficar apontado para a direção desejada"""
        while self.direcao != direcao_alvo:
            self.girar()

    def _validar_colisao(self, nova_posicao: Posicao) -> None:
        """VALIDAÇÃO CRÍTICA: Verifica se movimento causaria colisão"""
        if not self.labirinto.pode_mover_para(nova_posicao):
            # Determina tipo específico de problema
            sensor_destino = self.labirinto.ler_sensor(nova_posicao)
            
            if sensor_destino == TipoSensor.PAREDE:
                raise ColisaoException(
                    f"ALARME: Tentativa de colisão com parede na posição {nova_posicao}"
                )
            elif sensor_destino == TipoSensor.HUMANO:
                raise AtropelamentoException(
                    f"ALARME: Tentativa de atropelamento de humano na posição {nova_posicao}"
                )
    
    def _validar_beco_sem_saida(self) -> None:
        """VALIDAÇÃO CRÍTICA: Verifica se robô com humano está em beco sem saída"""
        if not self.tem_humano:
            return
        if self._esta_na_entrada():
            return
        
        # Conta quantos sensores veem parede
        sensores_parede = 0
        
        if self._ler_sensor_esquerdo() == TipoSensor.PAREDE:
            sensores_parede += 1
        if self._ler_sensor_direito() == TipoSensor.PAREDE:
            sensores_parede += 1
        if self._ler_sensor_frente() == TipoSensor.PAREDE:
            sensores_parede += 1
        
        # Se todos os 3 sensores veem parede, é beco sem saída
        if sensores_parede == 3:
            raise BecoSemSaidaException(
                "ALARME: Robô com humano em beco sem saída (claustrofobia!)"
            )
    
    def _validar_movimento_com_humano(self, nova_posicao: Posicao) -> None:
        """VALIDAÇÃO CRÍTICA: Verifica se movimento com humano levaria a beco sem saída"""
        if not self.tem_humano:
            return
        if self._esta_na_entrada(nova_posicao):
            return
        
        # Simula o movimento para verificar se resultaria em beco sem saída
        posicao_original = self.posicao
        direcao_original = self.direcao
        
        # Temporariamente simula estar na nova posição
        self.posicao = nova_posicao
        
        try:
            # Verifica todas as direções possíveis a partir da nova posição
            saidas_disponiveis = 0
            
            for direcao_teste in [Direcao.NORTE, Direcao.SUL, Direcao.LESTE, Direcao.OESTE]:
                self.direcao = direcao_teste
                posicao_teste = nova_posicao + direcao_teste.get_delta()
                
                # Se há pelo menos uma saída que não é parede, não é beco
                if self.labirinto.ler_sensor(posicao_teste) != TipoSensor.PAREDE:
                    saidas_disponiveis += 1
            
            # Se há apenas 1 saída disponível, pode ser um beco sem saída
            if saidas_disponiveis <= 1:
                raise BecoSemSaidaException(
                    f"ALARME: Movimento levaria robô com humano a beco sem saída (claustrofobia!) na posição {nova_posicao}"
                )
                
        finally:
            # Restaura posição e direção originais
            self.posicao = posicao_original
            self.direcao = direcao_original
    
    def avancar(self) -> None:
        """Comando A: Avança uma posição para frente"""
        if self.tem_humano and self._esta_na_entrada():
            raise OperacaoInvalidaException(
                "ALARME: Robô com humano na entrada deve ejetar antes de avançar!"
            )

        nova_posicao = self.posicao + self.direcao.get_delta()
        destino_eh_entrada = self._esta_na_entrada(nova_posicao)
        
        # VALIDAÇÃO CRÍTICA: Verifica colisões
        self._validar_colisao(nova_posicao)
        
        # VALIDAÇÃO CRÍTICA: Se tem humano, verifica se movimento leva a beco sem saída
        self._validar_movimento_com_humano(nova_posicao)
        
        # Move o robô
        self.posicao = nova_posicao

        if self.tem_humano and destino_eh_entrada:
            self._ajustar_orientacao_para_interior()
        
        # VALIDAÇÃO CRÍTICA: Verifica beco sem saída após movimento
        self._validar_beco_sem_saida()
        
        # Registra no log
        self._registrar_operacao(ComandoRobo.AVANCAR)
    
    def girar(self) -> None:
        """Comando G: Gira 90 graus à direita"""
        self.direcao = self.direcao.girar_direita()
        
        # VALIDAÇÃO CRÍTICA: Verifica beco sem saída após giro
        self._validar_beco_sem_saida()
        
        # Registra no log
        self._registrar_operacao(ComandoRobo.GIRAR)
    
    def pegar_humano(self) -> None:
        """Comando P: Pega o humano imediatamente à frente"""
        # VALIDAÇÃO CRÍTICA: Verifica se pode pegar
        if self.tem_humano:
            raise OperacaoInvalidaException(
                "ALARME: Tentativa de pegar humano, mas já tem um humano!"
            )
        
        # VALIDAÇÃO CRÍTICA: Só pode pegar se humano está À FRENTE (nunca na mesma posição)
        posicao_frente = self.posicao + self.direcao.get_delta()
        
        # Verifica se humano está APENAS à frente (evita atropelamento)
        humano_a_frente = self._ler_sensor_frente() == TipoSensor.HUMANO
        
        if not humano_a_frente:
            raise OperacaoInvalidaException(
                "ALARME: Tentativa de pegar humano, mas não há humano à frente!"
            )
        
        # Coleta o humano (APENAS da posição à frente)
        posicao_humano = posicao_frente
        
        if self.labirinto.coletar_humano(posicao_humano):
            self.tem_humano = True
        else:
            raise OperacaoInvalidaException(
                "ALARME: Falha ao coletar humano!"
            )
        
        # Registra no log
        self._registrar_operacao(ComandoRobo.PEGAR)
    
    def ejetar_humano(self) -> None:
        """Comando E: Ejeta o humano para fora do labirinto"""
        # VALIDAÇÃO CRÍTICA: Verifica se pode ejetar
        if not self.tem_humano:
            raise OperacaoInvalidaException(
                "ALARME: Tentativa de ejetar humano, mas não tem humano!"
            )
        
        # Deve estar na entrada para ejetar
        if self.posicao != self.labirinto.entrada:
            raise OperacaoInvalidaException(
                "ALARME: Tentativa de ejetar humano fora da entrada!"
            )

        # Ajusta orientação para saída antes da ejeção
        if self.direcao != self.direcao_saida:
            self._girar_para_direcao(self.direcao_saida)
        
        # Ejeta o humano
        if self.labirinto.ejetar_humano():
            self.tem_humano = False
        else:
            raise OperacaoInvalidaException(
                "ALARME: Falha ao ejetar humano!"
            )
        
        # Registra no log
        self._registrar_operacao(ComandoRobo.EJETAR)
    
    def _registrar_operacao(self, comando: ComandoRobo) -> None:
        """Registra uma operação no log após execução"""
        sensor_esquerdo = self._ler_sensor_esquerdo()
        sensor_direito = self._ler_sensor_direito()
        sensor_frente = self._ler_sensor_frente()
        status_carga = self._get_status_carga()
        
        self.logger.registrar_operacao(
            comando,
            sensor_esquerdo,
            sensor_direito,
            sensor_frente,
            status_carga
        )
    
    def executar_comando(self, comando: ComandoRobo) -> None:
        """Executa um comando específico com validações"""
        if comando == ComandoRobo.AVANCAR:
            self.avancar()
        elif comando == ComandoRobo.GIRAR:
            self.girar()
        elif comando == ComandoRobo.PEGAR:
            self.pegar_humano()
        elif comando == ComandoRobo.EJETAR:
            self.ejetar_humano()
        else:
            raise OperacaoInvalidaException(f"Comando inválido: {comando}")
    
    def get_estado_atual(self) -> Dict:
        """Retorna o estado atual do robô para debugging"""
        return {
            'posicao': self.posicao,
            'direcao': self.direcao,
            'tem_humano': self.tem_humano,
            'sensor_esquerdo': self._ler_sensor_esquerdo(),
            'sensor_direito': self._ler_sensor_direito(),
            'sensor_frente': self._ler_sensor_frente()
        }