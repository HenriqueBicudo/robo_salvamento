"""
Script de demonstração do robô de salvamento
Executa todos os mapas de teste e gera relatório
"""

import os
import sys
from pathlib import Path

# Adiciona src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from main import executar_missao, executar_todos_mapas
from tests.test_robo_salvamento import executar_todos_testes


def demonstrar_sistema():
    """Demonstra todas as funcionalidades do sistema"""
    print("🤖 DEMONSTRAÇÃO DO SISTEMA DE ROBÔ DE SALVAMENTO")
    print("=" * 60)
    print("Prof. Mozart Hasse - Serviços Cognitivos")
    print("Alunos: [ADICIONE SEUS NOMES E MATRÍCULAS AQUI]")
    print()
    
    # 1. Executa testes
    print("🧪 ETAPA 1: EXECUTANDO TESTES DE VALIDAÇÃO")
    print("-" * 40)
    sucesso_testes = executar_todos_testes()
    
    if not sucesso_testes:
        print("❌ Testes falharam! Corriga os problemas antes de continuar.")
        return False
    
    print("\n" + "="*60)
    
    # 2. Executa missões nos mapas de exemplo
    print("🚀 ETAPA 2: EXECUTANDO MISSÕES DE TESTE")
    print("-" * 40)
    
    mapas_teste = [
        "mapas/teste_simples.txt",
        "mapas/exemplo_professor.txt", 
        "mapas/teste_complexo.txt"
    ]
    
    sucessos = 0
    for mapa in mapas_teste:
        if os.path.exists(mapa):
            print(f"\n🎯 Testando: {mapa}")
            sucesso = executar_missao(mapa)
            if sucesso:
                sucessos += 1
        else:
            print(f"⚠️  Mapa não encontrado: {mapa}")
    
    print(f"\n📊 RESULTADO: {sucessos}/{len(mapas_teste)} missões bem-sucedidas")
    
    # 3. Exibe arquivos gerados
    print("\n" + "="*60)
    print("📁 ETAPA 3: ARQUIVOS GERADOS")
    print("-" * 40)
    
    if os.path.exists("logs"):
        logs = [f for f in os.listdir("logs") if f.endswith('.csv')]
        if logs:
            print("📄 Logs CSV gerados:")
            for log in sorted(logs):
                print(f"   • logs/{log}")
        else:
            print("ℹ️  Nenhum log encontrado")
    
    # 4. Instruções finais
    print("\n" + "="*60)
    print("📋 COMO USAR O SISTEMA")
    print("-" * 40)
    print("1. Para um mapa específico:")
    print("   python main.py mapas/seu_mapa.txt")
    print()
    print("2. Para executar testes:")
    print("   python tests/test_robo_salvamento.py")
    print()
    print("3. Para criar novos mapas:")
    print("   • Use X para paredes, . para espaços vazios")
    print("   • Use E para entrada, @ para humano")
    print("   • Entrada deve estar na borda")
    print()
    print("✅ Sistema pronto para uso!")
    
    return sucessos == len(mapas_teste)


if __name__ == "__main__":
    demonstrar_sistema()