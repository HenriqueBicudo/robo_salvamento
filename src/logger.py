"""
Sistema de logging CSV para auditoria do robô de salvamento
"""

import csv
import os
from typing import List
from .estruturas import ComandoRobo, TipoSensor, StatusCarga


class LoggerRobo:
    """Responsável por gerar logs CSV auditáveis da operação do robô"""
    
    def __init__(self, nome_arquivo_mapa: str, diretorio_logs: str = "logs"):
        """Inicializa o logger com base no nome do arquivo de mapa"""
        self.entradas: List[List[str]] = []
        
        # Gera nome do arquivo de log baseado no mapa
        nome_base = os.path.splitext(os.path.basename(nome_arquivo_mapa))[0]
        self.arquivo_log = os.path.join(diretorio_logs, f"{nome_base}.csv")
        
        # Garante que o diretório existe
        os.makedirs(diretorio_logs, exist_ok=True)
    
    def registrar_operacao(self, 
                          comando: ComandoRobo,
                          sensor_esquerdo: TipoSensor,
                          sensor_direito: TipoSensor,
                          sensor_frente: TipoSensor,
                          status_carga: StatusCarga) -> None:
        """Registra uma operação no log"""
        entrada = [
            comando.value,
            sensor_esquerdo.value,
            sensor_direito.value,
            sensor_frente.value,
            status_carga.value
        ]
        self.entradas.append(entrada)

    def salvar_log(self) -> None:
        """Salva o log em arquivo CSV"""
        try:
            with open(self.arquivo_log, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo)
                
                # Escreve todas as entradas
                for entrada in self.entradas:
                    writer.writerow(entrada)
                    
            print(f"Log salvo em: {self.arquivo_log}")
            
        except Exception as e:
            print(f"Erro ao salvar log: {e}")
    
    def get_nome_arquivo(self) -> str:
        """Retorna o nome do arquivo de log"""
        return self.arquivo_log
    
    def limpar(self) -> None:
        """Limpa todas as entradas do log"""
        self.entradas.clear()

    def get_sequencia_compacta(self) -> str:
        """Retorna a sequência compacta de comandos registrados (exclui LIGAR)."""
        comandos = [entrada[0] for entrada in self.entradas if entrada]
        letras = [cmd for cmd in comandos if len(cmd) == 1]
        return ''.join(letras)