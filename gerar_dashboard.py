#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Automação de Business Intelligence - Seguros
Gera dashboards diários a partir de arquivos Excel de comissões e produções

Autor: Sistema Automatizado
Data: 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, date
import re
import os
import sys
from pathlib import Path

# Configurações globais
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

# Paleta de cores corporativa
COLORS = {
    'primary': '#1e3a5f',
    'secondary': '#2e7d32',
    'accent': '#ff6f00',
    'light': '#e3f2fd',
    'dark': '#0d47a1',
    'success': '#4caf50',
    'warning': '#ff9800',
    'danger': '#f44336',
    'purple': '#7c4dff',
    'teal': '#009688'
}

# Cores por produto
PRODUCT_COLORS = {
    'Seguro de vida U': '#1565c0',
    'Seguro de vida M': '#0277bd', 
    'Dental': '#00897b',
    'Seguro Auto': '#ff8f00',
    'Seguro RE': '#7c4dff',
    'Seguro residencial': '#d84315'
}


def setup_directories():
    """Cria estrutura de diretórios necessária"""
    dirs = ['input', 'output', 'logs']
    for d in dirs:
        Path(d).mkdir(exist_ok=True)
    return dirs


def find_excel_files(input_dir='input'):
    """Encontra arquivos Excel no diretório de entrada"""
    input_path = Path(input_dir)
    files = list(input_path.glob('*.xlsx')) + list(input_path.glob('*.xls'))

    commission_file = None
    production_file = None

    for f in files:
        fname = f.name.lower()
        if 'comiss' in fname or 'gerente' in fname or 'porcentagem' in fname:
            commission_file = f
        elif 'produ' in fname or 'producao' in fname:
            production_file = f

    return commission_file, production_file


def parse_commission_data(file_path):
    """Processa dados de comissão do arquivo Excel"""
    try:
        commission_df = pd.read_excel(file_path, sheet_name=None)

        # Pega a primeira aba (geralmente "Março" ou mês atual)
        first_sheet = list(commission_df.keys())[0]
        marco_df = commission_df[first_sheet]

        managers_data = []

        for idx, row in marco_df.iterrows():
            if pd.notna(row.iloc[0]) and row.iloc[0] not in ['Seguro de vida U', 'Equipe']:
                manager = str(row.iloc[0]).strip()

                # Pega linha de porcentagens
                pct_row = row.iloc[1:].values

                # Pega linha de valores (próxima linha)
                if idx + 1 < len(marco_df):
                    val_row = marco_df.iloc[idx + 1].iloc[1:].values
                else:
                    val_row = [np.nan] * 6

                managers_data.append({
                    'Gerente': manager,
                    'Seguro de vida U (%)': float(pct_row[0]) if pd.notna(pct_row[0]) else 0,
                    'Seguro de vida U (R$)': float(val_row[0]) if pd.notna(val_row[0]) else 0,
                    'Seguro de vida M (%)': float(pct_row[1]) if pd.notna(pct_row[1]) else 0,
                    'Seguro de vida M (R$)': float(val_row[1]) if pd.notna(val_row[1]) else 0,
                    'Dental (%)': float(pct_row[2]) if pd.notna(pct_row[2]) else 0,
                    'Dental (R$)': float(val_row[2]) if pd.notna(val_row[2]) else 0,
                    'Seguro Auto (%)': float(pct_row[3]) if pd.notna(pct_row[3]) else 0,
                    'Seguro Auto (R$)': float(val_row[3]) if pd.notna(val_row[3]) else 0,
                    'Seguro RE (%)': float(pct_row[4]) if pd.notna(pct_row[4]) else 0,
                    'Seguro RE (R$)': float(val_row[4]) if pd.notna(val_row[4]) else 0,
                    'Seguro residencial (%)': float(pct_row[5]) if pd.notna(pct_row[5]) else 0,
                    'Seguro residencial (R$)': float(val_row[5]) if pd.notna(val_row[5]) else 0,
                })

        commission_summary = pd.DataFrame(managers_data)

        # Calcula total de comissão
        commission_summary['Total_Comissao'] = (
            commission_summary['Seguro de vida U (R$)'] + 
            commission_summary['Seguro de vida M (R$)'] + 
            commission_summary['Dental (R$)'] + 
            commission_summary['Seguro Auto (R$)'] + 
            commission_summary['Seguro RE (R$)'] + 
            commission_summary['Seguro residencial (R$)']
        )

        return commission_summary

    except Exception as e:
        print(f"Erro ao processar comissões: {e}")
        return None


def parse_production_data(file_path):
    """Processa dados de produção do arquivo Excel"""
    try:
        production_df = pd.read_excel(file_path, sheet_name=None)
        productions_list = []

        for sheet_name in production_df.keys():
            df = production_df[sheet_name]

            # Parse da data do nome da aba
            date_str = sheet_name.lower()
            current_year = datetime.now().year

            # Padrões de data comuns
            date_patterns = [
                (r'(\d{1,2})[\/\-]?(\d{1,2})', lambda m: f"{current_year}-{int(m.group(2)):02d}-{int(m.group(1)):02d}"),
                (r'(\d{1,2})(jan|fev|mar|abr|mai|jun|jul|ago|set|out|nov|dez)', 
                 lambda m: f"{current_year}-{parse_month(m.group(2))}-{int(m.group(1)):02d}"),
                (r'(\d{1,2})(janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)', 
                 lambda m: f"{current_year}-{parse_month(m.group(2))}-{int(m.group(1)):02d}"),
            ]

            parsed_date = None
            for pattern, formatter in date_patterns:
                match = re.search(pattern, date_str)
                if match:
                    try:
                        parsed_date = formatter(match)
                        break
                    except:
                        continue

            if not parsed_date:
                parsed_date = f"{current_year}-01-01"  # Data padrão

            # Processa registros de produção
            values = df.iloc[:, 0].tolist()

            i = 0
            while i < len(values):
                if pd.notna(values[i]) and 'produto' in str(values[i]).lower():
                    produto = str(values[i]).split('-')[-1].strip() if '-' in str(values[i]) else str(values[i]).replace('Produto-', '').strip()

                    # Extrai próximos campos
                    gerente = extract_field(values, i + 1, ['gr', 'gerente'])
                    cliente = extract_field(values, i + 2, ['cliente'])
                    proposta = extract_field(values, i + 3, ['proposta'])
                    valor = extract_value(values, i + 4)

                    productions_list.append({
                        'Data': parsed_date,
                        'Produto': produto,
                        'Gerente': gerente,
                        'Cliente': cliente,
                        'Proposta': proposta,
                        'Valor': valor
                    })
                    i += 5
                else:
                    i += 1

        return pd.DataFrame(productions_list)

    except Exception as e:
        print(f"Erro ao processar produções: {e}")
        return None


def parse_month(month_str):
    """Converte nome do mês para número"""
    months = {
        'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
        'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12,
        'janeiro': 1, 'fevereiro': 2, 'março': 3, 'abril': 4, 'maio': 5, 'junho': 6,
        'julho': 7, 'agosto': 8, 'setembro': 9, 'outubro': 10, 'novembro': 11, 'dezembro': 12
    }
    return months.get(month_str.lower(), 1)


def extract_field(values, index, prefixes):
    """Extrai campo baseado em prefixos"""
    if index < len(values) and pd.notna(values[index]):
        text = str(values[index])
        for prefix in prefixes:
            pattern = re.compile(f'{prefix}[\-\s]*(.+)', re.IGNORECASE)
            match = pattern.search(text)
            if match:
                return match.group(1).strip()
        return text
    return ''


def extract_value(values, index):
    """Extrai valor monetário"""
    if index < len(values) and pd.notna(values[index]):
        text = str(values[index])
        match = re.search(r'[\d.,]+', text.replace('.', '').replace(',', '.'))
        if match:
            try:
                return float(match.group().replace(',', '.'))
            except:
                return 0
    return 0


def create_main_dashboard(commission_df, production_df, output_dir='output'):
    """Cria o dashboard principal"""
    fig = plt.figure(figsize=(20, 24))

    # KPI Cards
    total_producao = production_df['Valor'].sum() if production_df is not None else 0
    total_propostas = len(production_df) if production_df is not None else 0
    ticket_medio = production_df['Valor'].mean() if production_df is not None and len(production_df) > 0 else 0

    # KPI 1
    ax_kpi = fig.add_subplot(6, 3, 1)
    ax_kpi.axis('off')
    ax_kpi.set_xlim(0, 10)
    ax_kpi.set_ylim(0, 10)
    ax_kpi.add_patch(plt.Rectangle((0, 0), 10, 10, facecolor=COLORS['primary'], alpha=0.9))
    ax_kpi.text(5, 7, f'R$ {total_producao:,.2f}', fontsize=28, ha='center', va='center', color='white', weight='bold')
    ax_kpi.text(5, 4, 'Total Produção', fontsize=14, ha='center', va='center', color='white')
    ax_kpi.text(5, 2, f'Atualizado: {datetime.now().strftime("%d/%m/%Y")}', fontsize=11, ha='center', va='center', color='white', alpha=0.7)

    # KPI 2
    ax_kpi2 = fig.add_subplot(6, 3, 2)
    ax_kpi2.axis('off')
    ax_kpi2.set_xlim(0, 10)
    ax_kpi2.set_ylim(0, 10)
    ax_kpi2.add_patch(plt.Rectangle((0, 0), 10, 10, facecolor=COLORS['secondary'], alpha=0.9))
    ax_kpi2.text(5, 7, str(total_propostas), fontsize=28, ha='center', va='center', color='white', weight='bold')
    ax_kpi2.text(5, 4, 'Propostas Emitidas', fontsize=14, ha='center', va='center', color='white')
    ax_kpi2.text(5, 2, f'{production_df["Gerente"].nunique() if production_df is not None else 0} Gerentes Ativos', fontsize=11, ha='center', va='center', color='white', alpha=0.7)

    # KPI 3
    ax_kpi3 = fig.add_subplot(6, 3, 3)
    ax_kpi3.axis('off')
    ax_kpi3.set_xlim(0, 10)
    ax_kpi3.set_ylim(0, 10)
    ax_kpi3.add_patch(plt.Rectangle((0, 0), 10, 10, facecolor=COLORS['accent'], alpha=0.9))
    ax_kpi3.text(5, 7, f'R$ {ticket_medio:,.2f}', fontsize=28, ha='center', va='center', color='white', weight='bold')
    ax_kpi3.text(5, 4, 'Ticket Médio', fontsize=14, ha='center', va='center', color='white')
    if production_df is not None and len(production_df) > 0:
        top_prod = production_df.loc[production_df['Valor'].idxmax()]
        ax_kpi3.text(5, 2, f'{top_prod["Produto"]}: Maior ticket', fontsize=11, ha='center', va='center', color='white', alpha=0.7)

    # Gráficos de produção
    if production_df is not None and len(production_df) > 0:
        # Produção por produto
        ax1 = fig.add_subplot(6, 3, 4)
        product_summary = production_df.groupby('Produto')['Valor'].sum().sort_values(ascending=True)
        bars = ax1.barh(product_summary.index, product_summary.values, color=COLORS['primary'])
        ax1.set_xlabel('Valor (R$)', fontsize=11, weight='bold')
        ax1.set_title('Produção por Produto', fontsize=14, weight='bold', pad=15)
        for i, (idx, val) in enumerate(product_summary.items()):
            ax1.text(val + 50, i, f'R$ {val:,.0f}', va='center', fontsize=10, weight='bold')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        # Produção por gerente
        ax2 = fig.add_subplot(6, 3, 5)
        manager_summary = production_df.groupby('Gerente')['Valor'].sum().sort_values(ascending=True)
        bars = ax2.barh(manager_summary.index, manager_summary.values, color=COLORS['primary'])
        ax2.set_xlabel('Valor (R$)', fontsize=11, weight='bold')
        ax2.set_title('Produção por Gerente', fontsize=14, weight='bold', pad=15)
        for i, (idx, val) in enumerate(manager_summary.items()):
            ax2.text(val + 50, i, f'R$ {val:,.0f}', va='center', fontsize=10, weight='bold')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        # Timeline
        ax3 = fig.add_subplot(6, 3, 6)
        production_df['Data_dt'] = pd.to_datetime(production_df['Data'])
        timeline = production_df.groupby('Data_dt')['Valor'].sum()
        ax3.plot(timeline.index, timeline.values, marker='o', linewidth=3, markersize=10, color=COLORS['primary'])
        ax3.fill_between(timeline.index, timeline.values, alpha=0.3, color=COLORS['primary'])
        ax3.set_title('Evolução Temporal', fontsize=14, weight='bold', pad=15)
        ax3.tick_params(axis='x', rotation=45)
        ax3.grid(True, alpha=0.3)

    # Gráficos de comissão
    if commission_df is not None:
        # Top gerentes
        ax4 = fig.add_subplot(6, 3, 7)
        top_managers = commission_df.nlargest(8, 'Total_Comissao')
        ax4.barh(top_managers['Gerente'], top_managers['Total_Comissao'], color=COLORS['secondary'])
        ax4.set_xlabel('Total Comissão (R$)', fontsize=11, weight='bold')
        ax4.set_title('Top Gerentes - Comissão', fontsize=14, weight='bold', pad=15)
        ax4.spines['top'].set_visible(False)
        ax4.spines['right'].set_visible(False)

        # Distribuição por produto
        ax5 = fig.add_subplot(6, 3, 8)
        products = ['Vida U', 'Vida M', 'Dental', 'Auto', 'RE', 'Residencial']
        commission_values = [
            commission_df['Seguro de vida U (R$)'].sum(),
            commission_df['Seguro de vida M (R$)'].sum(),
            commission_df['Dental (R$)'].sum(),
            commission_df['Seguro Auto (R$)'].sum(),
            commission_df['Seguro RE (R$)'].sum(),
            commission_df['Seguro residencial (R$)'].sum()
        ]
        ax5.pie(commission_values, labels=products, autopct='%1.1f%%', colors=list(PRODUCT_COLORS.values()))
        ax5.set_title('Distribuição por Produto', fontsize=14, weight='bold', pad=15)

        # Taxas médias
        ax6 = fig.add_subplot(6, 3, 9)
        avg_rates = [
            commission_df['Seguro de vida U (%)'].mean(),
            commission_df['Seguro de vida M (%)'].mean(),
            commission_df['Dental (%)'].mean(),
            commission_df['Seguro Auto (%)'].mean(),
            commission_df['Seguro RE (%)'].mean(),
            commission_df['Seguro residencial (%)'].mean()
        ]
        ax6.bar(products, avg_rates, color=list(PRODUCT_COLORS.values()))
        ax6.set_ylabel('Taxa Média (%)', fontsize=11, weight='bold')
        ax6.set_title('Taxa Média de Comissão', fontsize=14, weight='bold', pad=15)
        ax6.tick_params(axis='x', rotation=45)

    plt.suptitle('DASHBOARD DE BUSINESS INTELLIGENCE - SEGUROS', fontsize=24, weight='bold', y=0.98, color=COLORS['primary'])
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # Salva arquivo
    today = datetime.now().strftime('%Y%m%d')
    output_path = Path(output_dir) / f'bi_dashboard_seguros_{today}.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"Dashboard principal salvo: {output_path}")
    return output_path


def create_commission_dashboard(commission_df, production_df, output_dir='output'):
    """Cria dashboard detalhado de comissões"""
    fig = plt.figure(figsize=(20, 16))

    if commission_df is not None:
        # Heatmap
        ax1 = fig.add_subplot(3, 3, 1)
        heatmap_data = commission_df.set_index('Gerente')[[
            'Seguro de vida U (R$)', 'Seguro de vida M (R$)', 'Dental (R$)',
            'Seguro Auto (R$)', 'Seguro RE (R$)', 'Seguro residencial (R$)'
        ]].values

        im = ax1.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
        ax1.set_xticks(range(6))
        ax1.set_xticklabels(['Vida U', 'Vida M', 'Dental', 'Auto', 'RE', 'Resid.'], rotation=45, ha='right')
        ax1.set_yticks(range(len(commission_df)))
        ax1.set_yticklabels(commission_df['Gerente'], fontsize=9)
        ax1.set_title('Mapa de Calor - Comissões', fontsize=14, weight='bold', pad=15)
        plt.colorbar(im, ax=ax1, fraction=0.046)

        # Top 5
        ax3 = fig.add_subplot(3, 3, 3)
        top_5 = commission_df.nlargest(5, 'Total_Comissao')
        ax3.bar(range(len(top_5)), top_5['Total_Comissao'], color=COLORS['primary'])
        ax3.set_xticks(range(len(top_5)))
        ax3.set_xticklabels(top_5['Gerente'], rotation=45, ha='right')
        ax3.set_title('Top 5 Gerentes', fontsize=14, weight='bold', pad=15)

    plt.suptitle('ANÁLISE DETALHADA DE COMISSÕES', fontsize=22, weight='bold', y=0.98, color=COLORS['primary'])
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    today = datetime.now().strftime('%Y%m%d')
    output_path = Path(output_dir) / f'bi_comissoes_detalhado_{today}.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"Dashboard de comissões salvo: {output_path}")
    return output_path


def log_execution(message, log_dir='logs'):
    """Registra execução em log"""
    log_file = Path(log_dir) / f'execucao_{datetime.now().strftime("%Y%m")}.log'
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {message}\n')


def main():
    """Função principal"""
    print("=" * 60)
    print("DASHBOARD AUTOMATIZADO - SEGUROS")
    print(f"Execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)

    # Setup
    setup_directories()

    # Encontra arquivos
    commission_file, production_file = find_excel_files('input')

    if not commission_file and not production_file:
        print("ERRO: Nenhum arquivo Excel encontrado na pasta 'input'")
        print("Por favor, coloque os arquivos na pasta 'input' e execute novamente.")
        log_execution("ERRO: Arquivos não encontrados")
        return 1

    print(f"\nArquivos encontrados:")
    if commission_file:
        print(f"  ✓ Comissões: {commission_file.name}")
    if production_file:
        print(f"  ✓ Produções: {production_file.name}")

    # Processa dados
    commission_df = parse_commission_data(commission_file) if commission_file else None
    production_df = parse_production_data(production_file) if production_file else None

    # Gera dashboards
    if commission_df is not None or production_df is not None:
        print("\nGerando dashboards...")
        create_main_dashboard(commission_df, production_df)
        create_commission_dashboard(commission_df, production_df)
        print("\n✓ Dashboards gerados com sucesso!")
        log_execution("Dashboards gerados com sucesso")
    else:
        print("\n✗ Erro ao processar dados")
        log_execution("ERRO: Falha no processamento dos dados")
        return 1

    print(f"\nArquivos salvos em: {Path('output').absolute()}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
