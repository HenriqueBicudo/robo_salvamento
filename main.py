"""
Arquivo principal do simulador do robô de salvamento
Executa missões completas de busca e salvamento
Autor: [SEU NOME E MATRÍCULA AQUI]
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.labirinto import Labirinto
from src.robo import Robo
from src.logger import LoggerRobo
from src.algoritmo_busca import AlgoritmoBusca
from src.estruturas import RoboException


def executar_missao(arquivo_mapa: str, diretorio_logs: str = "logs") -> bool:
    """Executa uma missão completa de busca e salvamento"""
    try:
        print(f"\n{'='*60}")
        print(f"🚀 INICIANDO MISSÃO: {os.path.basename(arquivo_mapa)}")
        print(f"{'='*60}")
        
        # Inicializa componentes
        print("⚙️  Inicializando componentes...")
        labirinto = Labirinto(arquivo_mapa)
        logger = LoggerRobo(arquivo_mapa, diretorio_logs)
        robo = Robo(labirinto, logger)
        algoritmo = AlgoritmoBusca(robo)
        
        print(f"📍 Entrada encontrada em: ({labirinto.entrada.x}, {labirinto.entrada.y})")
        print(f"👤 Humano localizado em: ({labirinto.posicao_humano.x}, {labirinto.posicao_humano.y})")
        print(f"📊 Dimensões do labirinto: {labirinto.largura}x{labirinto.altura}")
        
        # Executa missão
        sucesso = algoritmo.executar_missao()
        
        # Salva log
        logger.salvar_log()
        
        # Exibe estatísticas
        stats = algoritmo.get_estatisticas()
        print(f"\n📈 ESTATÍSTICAS DA MISSÃO:")
        print(f"   • Posições visitadas: {stats['posicoes_visitadas']}")
        print(f"   • Posições conhecidas: {stats['posicoes_conhecidas']}")
        print(f"   • Movimentos realizados: {stats['caminho_percorrido']}")
        print(f"   • Humano encontrado: {'✅' if stats['humano_encontrado'] else '❌'}")
        print(f"   • Humano coletado: {'✅' if stats['humano_coletado'] else '❌'}")
        print(f"   • Missão concluída: {'✅' if stats['missao_concluida'] else '❌'}")
        
        if sucesso:
            print(f"\n🎉 MISSÃO CONCLUÍDA COM SUCESSO!")
            print(f"📄 Log salvo em: {logger.get_nome_arquivo()}")
        else:
            print(f"\n💥 MISSÃO FALHOU!")
        
        return sucesso
        
    except RoboException as e:
        print(f"\n⚠️  ERRO DO ROBÔ: {e}")
        return False
    except Exception as e:
        print(f"\n💥 ERRO GERAL: {e}")
        return False


def main():
    """Função principal"""
    print("🤖 SIMULADOR DO ROBÔ DE SALVAMENTO")
    print("Prof. Mozart Hasse - Serviços Cognitivos")
    print("Alunos: [ADICIONE SEUS NOMES E MATRÍCULAS AQUI]")
    
    # Verifica argumentos da linha de comando
    if len(sys.argv) < 2:
        print(f"\n❌ Uso: {sys.argv[0]} <arquivo_mapa> [diretorio_logs]")
        print(f"Exemplo: {sys.argv[0]} mapas/exemplo.txt logs")
        return
    
    arquivo_mapa = sys.argv[1]
    diretorio_logs = sys.argv[2] if len(sys.argv) > 2 else "logs"
    
    # Verifica se arquivo existe
    if not os.path.exists(arquivo_mapa):
        print(f"❌ Arquivo não encontrado: {arquivo_mapa}")
        return
    
    # Executa missão
    sucesso = executar_missao(arquivo_mapa, diretorio_logs)
    
    # Código de saída
    sys.exit(0 if sucesso else 1)


def executar_todos_mapas(diretorio_mapas: str = "mapas"):
    """Executa missões para todos os mapas em um diretório"""
    if not os.path.exists(diretorio_mapas):
        print(f"❌ Diretório não encontrado: {diretorio_mapas}")
        return
    
    arquivos_mapa = [f for f in os.listdir(diretorio_mapas) 
                     if f.endswith('.txt')]
    
    if not arquivos_mapa:
        print(f"❌ Nenhum arquivo .txt encontrado em {diretorio_mapas}")
        return
    
    sucessos = 0
    total = len(arquivos_mapa)
    
    print(f"\n🔄 Executando {total} missões...")
    
    for arquivo in sorted(arquivos_mapa):
        caminho_completo = os.path.join(diretorio_mapas, arquivo)
        sucesso = executar_missao(caminho_completo)
        if sucesso:
            sucessos += 1
    
    print(f"\n📊 RESULTADO FINAL: {sucessos}/{total} missões bem-sucedidas")
    print(f"Taxa de sucesso: {(sucessos/total)*100:.1f}%")


if __name__ == "__main__":
    main()