@echo off
echo 🤖 ROBÔ DE SALVAMENTO - SISTEMA EMBARCADO
echo =========================================
echo Prof. Mozart Hasse - Serviços Cognitivos
echo **Aluno:** [Enzo Luiz Berlesi Salles - RA:2023102306]
echo **Aluno:** [Joao Pedro Calixto Godoy - RA:2023100923]
echo **Aluno:** [Henrique Bicudo - RA:2023103607]
echo.

REM Verifica se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale Python 3.7+ primeiro.
    pause
    exit /b 1
)

echo ✅ Python encontrado!
echo.

REM Executa demonstração completa
echo 🚀 Executando demonstração completa...
echo.
python demo.py

echo.
echo 📋 COMANDOS DISPONÍVEIS:
echo.
echo 1. Executar mapa específico:
echo    python main.py mapas\exemplo_professor.txt
echo.
echo 2. Executar testes:
echo    python tests\test_robo_salvamento.py
echo.
echo 3. Demonstração completa:
echo    python demo.py
echo.
echo ✅ Sistema pronto para uso!
pause