#!/bin/bash
# Script de agendamento para gerar dashboards diários
# 
# INSTALAÇÃO:
# 1. Copie este arquivo para o diretório do projeto
# 2. Dê permissão de execução: chmod +x agendar_dashboard.sh
# 3. Execute: ./agendar_dashboard.sh
#
# REQUISITOS:
# - Python 3.7+
# - pip install pandas matplotlib openpyxl

DIRETORIO_PROJETO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CRON_JOB="0 8 * * * cd $DIRETORIO_PROJETO && /usr/bin/python3 $DIRETORIO_PROJETO/gerar_dashboard.py >> $DIRETORIO_PROJETO/logs/cron.log 2>&1"

echo "=========================================="
echo "AGENDADOR DE DASHBOARD - SEGUROS"
echo "=========================================="
echo ""
echo "Diretório do projeto: $DIRETORIO_PROJETO"
echo ""

# Verifica se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "ERRO: Python 3 não encontrado!"
    echo "Por favor, instale o Python 3.7 ou superior."
    exit 1
fi

# Verifica dependências
echo "Verificando dependências..."
python3 -c "import pandas, matplotlib, openpyxl" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Instalando dependências..."
    pip3 install pandas matplotlib openpyxl
fi

# Cria estrutura de diretórios
mkdir -p "$DIRETORIO_PROJETO/input"
mkdir -p "$DIRETORIO_PROJETO/output"
mkdir -p "$DIRETORIO_PROJETO/logs"

echo ""
echo "Escolha uma opção:"
echo "1. Executar agora (uma vez)"
echo "2. Agendar execução diária (08:00)"
echo "3. Agendar execução diária (hora personalizada)"
echo "4. Remover agendamento"
echo "5. Sair"
echo ""
read -p "Opção: " opcao

case $opcao in
    1)
        echo "Executando dashboard..."
        cd "$DIRETORIO_PROJETO"
        python3 gerar_dashboard.py
        ;;
    2)
        # Remove job antigo se existir
        crontab -l 2>/dev/null | grep -v "gerar_dashboard.py" | crontab -
        # Adiciona novo job
        (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
        echo "✓ Agendamento criado: todos os dias às 08:00"
        echo "  Para verificar: crontab -l"
        ;;
    3)
        read -p "Hora (0-23): " hora
        read -p "Minuto (0-59): " minuto
        CRON_CUSTOM="$minuto $hora * * * cd $DIRETORIO_PROJETO && /usr/bin/python3 $DIRETORIO_PROJETO/gerar_dashboard.py >> $DIRETORIO_PROJETO/logs/cron.log 2>&1"
        crontab -l 2>/dev/null | grep -v "gerar_dashboard.py" | crontab -
        (crontab -l 2>/dev/null; echo "$CRON_CUSTOM") | crontab -
        echo "✓ Agendamento criado: todos os dias às $(printf "%02d:%02d" $hora $minuto)"
        ;;
    4)
        crontab -l 2>/dev/null | grep -v "gerar_dashboard.py" | crontab -
        echo "✓ Agendamento removido"
        ;;
    5)
        echo "Saindo..."
        exit 0
        ;;
    *)
        echo "Opção inválida"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "Estrutura de diretórios criada:"
echo "  input/   - Coloque os arquivos Excel aqui"
echo "  output/  - Dashboards serão salvos aqui"
echo "  logs/    - Logs de execução"
echo "=========================================="
