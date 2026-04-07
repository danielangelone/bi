@echo off
chcp 65001 >nul
echo ==========================================
echo AGENDADOR DE DASHBOARD - SEGUROS (Windows)
echo ==========================================
echo.

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

:: Verifica Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERRO: Python nao encontrado!
    echo Por favor, instale o Python 3.7 ou superior.
    pause
    exit /b 1
)

:: Verifica/Instala dependencias
echo Verificando dependencias...
python -c "import pandas, matplotlib, openpyxl" 2>nul
if errorlevel 1 (
    echo Instalando dependencias...
    pip install pandas matplotlib openpyxl
)

:: Cria diretorios
if not exist "input" mkdir input
if not exist "output" mkdir output
if not exist "logs" mkdir logs

echo.
echo Escolha uma opcao:
echo 1. Executar agora (uma vez)
echo 2. Agendar execucao diaria (08:00)
echo 3. Abrir Agendador de Tarefas (manual)
echo 4. Remover agendamento
echo 5. Sair
echo.
set /p opcao="Opcao: "

if "%opcao%"=="1" goto executar
if "%opcao%"=="2" goto agendar
if "%opcao%"=="3" goto manual
if "%opcao%"=="4" goto remover
if "%opcao%"=="5" goto fim

echo Opcao invalida!
pause
exit /b 1

:executar
echo Executando dashboard...
python gerar_dashboard.py
pause
goto fim

:agendar
echo Criando tarefa agendada...
schtasks /create /tn "DashboardSeguros" /tr "'%SCRIPT_DIR%run_dashboard.bat'" /sc daily /st 08:00 /f >nul 2>&1
if errorlevel 1 (
    echo Tentando com privilegios elevados...
    powershell -Command "Start-Process schtasks -ArgumentList '/create /tn DashboardSeguros /tr "%SCRIPT_DIR%run_dashboard.bat" /sc daily /st 08:00 /f' -Verb runAs"
)
echo ✓ Tarefa agendada para 08:00 diariamente
echo   Para verificar: Painel de Controle ^> Ferramentas Administrativas ^> Agendador de Tarefas
pause
goto fim

:manual
start taskschd.msc
goto fim

:remover
schtasks /delete /tn "DashboardSeguros" /f >nul 2>&1
echo ✓ Agendamento removido
pause
goto fim

:fim
echo.
echo ==========================================
echo Estrutura de diretorios:
echo   input/   - Coloque os arquivos Excel aqui
echo   output/  - Dashboards serao salvos aqui
echo   logs/    - Logs de execucao
echo ==========================================
pause
