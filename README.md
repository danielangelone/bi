# Dashboard Automatizado - Seguros

Sistema de Business Intelligence automatizado para geração de dashboards de comissões e produções de seguros.

## 📁 Estrutura de Arquivos

```
projeto-dashboard/
├── gerar_dashboard.py      # Script principal (Python)
├── agendar_dashboard.sh    # Agendador Linux/Mac
├── agendar_dashboard.bat   # Agendador Windows
├── run_dashboard.bat       # Executor Windows
├── input/                  # Coloque os arquivos Excel aqui
├── output/                 # Dashboards gerados (PNG)
└── logs/                   # Logs de execução
```

## 🚀 Instalação Rápida

### Linux/Mac
```bash
# 1. Dê permissão de execução
chmod +x agendar_dashboard.sh

# 2. Execute o agendador
./agendar_dashboard.sh
```

### Windows
```cmd
# 1. Execute o agendador (como Administrador)
agendar_dashboard.bat
```

## 📊 Formato dos Arquivos Excel

### Arquivo de Comissões
- **Nome sugerido**: `comissao_gerentes.xlsx` ou `porcentagem_comissao.xlsx`
- **Estrutura**: Aba com nome do mês (ex: "Março")
- **Formato**: 
  - Linha 1: Nomes dos produtos (Vida U, Vida M, Dental, Auto, RE, Residencial)
  - Linhas seguintes: Gerente | % Comissão | (próxima linha) Valor R$

### Arquivo de Produções
- **Nome sugerido**: `producoes.xlsx` ou `producoes_diarias.xlsx`
- **Estrutura**: Abas nomeadas com datas (ex: "25março", "01abril")
- **Formato por registro**:
  ```
  Produto-[Tipo]
  Gr-[Nome Gerente]
  Cliente-[Nome Cliente]
  Proposta-[Número]
  Valor líquido- [Valor]
  ```

## ⚙️ Modos de Uso

### 1. Execução Manual (Uma Vez)
**Linux/Mac:**
```bash
python3 gerar_dashboard.py
```

**Windows:**
```cmd
python gerar_dashboard.py
```

Ou execute `agendar_dashboard.sh`/`agendar_dashboard.bat` e escolha opção 1.

### 2. Agendamento Diário Automático

**Linux/Mac (Cron):**
```bash
./agendar_dashboard.sh
# Escolha opção 2 (08:00) ou 3 (horário personalizado)
```

**Windows (Task Scheduler):**
```cmd
agendar_dashboard.bat
# Escolha opção 2
```

### 3. Agendamento Manual Avançado

**Linux - Editar crontab:**
```bash
crontab -e
# Adicione:
0 8 * * * cd /caminho/do/projeto && python3 gerar_dashboard.py
```

**Windows - Task Scheduler:**
1. Abra `taskschd.msc`
2. Crie nova tarefa básica
3. Programa: `python` ou `python.exe`
4. Argumentos: `gerar_dashboard.py`
5. Iniciar em: `[caminho completo do projeto]`

## 📅 Frequência de Execução

| Opção | Comando Cron | Descrição |
|-------|--------------|-----------|
| Diário 08:00 | `0 8 * * *` | Padrão recomendado |
| Diário 18:00 | `0 18 * * *` | Fim do expediente |
| A cada 6h | `0 */6 * * *` | Alta frequência |
| Seg-Sex 09:00 | `0 9 * * 1-5` | Dias úteis apenas |

## 🔧 Requisitos

- **Python**: 3.7 ou superior
- **Bibliotecas**: pandas, matplotlib, openpyxl

**Instalação das dependências:**
```bash
pip install pandas matplotlib openpyxl
```

## 📈 Saídas Geradas

A cada execução, são gerados 2 arquivos PNG na pasta `output/`:

1. `bi_dashboard_seguros_YYYYMMDD.png` - Dashboard principal com KPIs e visão geral
2. `bi_comissoes_detalhado_YYYYMMDD.png` - Análise detalhada de comissões

## 🐛 Solução de Problemas

### Erro: "Arquivos não encontrados"
- Verifique se os arquivos Excel estão na pasta `input/`
- Nomes aceitos: qualquer arquivo .xlsx contendo "comiss", "gerente", "produ" ou "producao"

### Erro: "ModuleNotFoundError"
```bash
pip install pandas matplotlib openpyxl
```

### Erro de codificação (Windows)
Execute no PowerShell:
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
python gerar_dashboard.py
```

### Logs de erro
Verifique o arquivo `logs/execucao_YYYYMM.log` para detalhes de erros.

## 📝 Notas

- O script detecta automaticamente os arquivos Excel na pasta `input/`
- As datas nos nomes das abas são interpretadas automaticamente
- Dashboards antigos não são sobrescritos (nome inclui data)
- Execute manualmente antes de agendar para testar

## 🔄 Atualização

Para atualizar o script, substitua apenas o arquivo `gerar_dashboard.py` mantendo a pasta `input/` com seus dados.

---

**Desenvolvido para**: Automação de relatórios de seguros  
**Versão**: 1.0  
**Data**: 2024
