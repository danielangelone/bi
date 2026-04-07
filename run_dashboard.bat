@echo off
cd /d "%~dp0"
python gerar_dashboard.py >> logs\cron.log 2>&1
