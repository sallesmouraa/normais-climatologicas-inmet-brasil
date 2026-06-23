"""
Script para harmonizar dados climatológicos do formato "longo" (por variável e mês)
para formato "largo" (consolidado por município/estado).

Transforma os dados brutos do INMET em um formato amigável para API e Dashboard.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# Mapping de UF para região do Brasil
UF_TO_REGIAO = {
    'AC': 'Norte', 'AM': 'Norte', 'AP': 'Norte', 'PA': 'Norte', 'RO': 'Norte', 'RR': 'Norte', 'TO': 'Norte',
    'AL': 'Nordeste', 'BA': 'Nordeste', 'CE': 'Nordeste', 'MA': 'Nordeste', 'PB': 'Nordeste', 'PE': 'Nordeste', 'PI': 'Nordeste', 'RN': 'Nordeste', 'SE': 'Nordeste',
    'DF': 'Centro-Oeste', 'GO': 'Centro-Oeste', 'MS': 'Centro-Oeste', 'MT': 'Centro-Oeste',
    'ES': 'Sudeste', 'MG': 'Sudeste', 'RJ': 'Sudeste', 'SP': 'Sudeste',
    'PR': 'Sul', 'RS': 'Sul', 'SC': 'Sul',
}

# Mapping de variáveis climáticas para nomes padronizados
VARIAVEL_MAPPING = {
    'temperatura_media': 'temperatura_media',
    'temperatura_maxima': 'temperatura_maxima',
    'temperatura_minima': 'temperatura_minima',
    'precipitacao': 'precipitacao_media',
    'umidade_relativa': 'umidade_relativa',
}


def harmonizar_dados(input_csv: str, output_csv: str) -> pd.DataFrame:
    """
    Transforma dados do formato longo para formato consolidado por município.
    
    Args:
        input_csv: Caminho do CSV bruto (formato longo)
        output_csv: Caminho do CSV harmonizado (formato largo)
    
    Returns:
        DataFrame harmonizado
    """
    print(f"📖 Lendo dados de {input_csv}...")
    df = pd.read_csv(input_csv)
    
    print("🔄 Harmonizando dados...")
    
    # Pivot: agrupa por estação e variável climatica
    pivot_data = df.pivot_table(
        index=['codigo_estacao', 'nome_estacao', 'uf'],
        columns='variavel_climatica',
        values='valor_variavel',
        aggfunc='mean'  # Média de todos os meses
    ).reset_index()
    
    # Normalizar nomes de colunas de variáveis
    for col in pivot_data.columns:
        if col not in ['codigo_estacao', 'nome_estacao', 'uf']:
            # Converter para snake_case e padronizar
            col_normalized = col.lower().replace(' ', '_').replace('-', '_')
            if col_normalized in VARIAVEL_MAPPING:
                pivot_data.rename(columns={col: VARIAVEL_MAPPING[col_normalized]}, inplace=True)
    
    # Adicionar coluna de estado (UF já existe, renomear para "estado")
    pivot_data.rename(columns={'uf': 'estado'}, inplace=True)
    
    # Adicionar coluna de região
    pivot_data['regiao'] = pivot_data['estado'].map(UF_TO_REGIAO)
    
    # Renomear nome_estacao para municipio
    pivot_data.rename(columns={'nome_estacao': 'municipio'}, inplace=True)
    
    # Adicionar colunas de latitude/longitude (placeholder: será melhorado após)
    pivot_data['latitude'] = np.nan
    pivot_data['longitude'] = np.nan
    
    # Reordenar colunas de forma intuitiva
    coluna_ordem = [
        'codigo_estacao',
        'municipio',
        'estado',
        'regiao',
        'latitude',
        'longitude',
        'temperatura_media',
        'temperatura_maxima',
        'temperatura_minima',
        'precipitacao_media',
        'umidade_relativa'
    ]
    
    # Manter apenas colunas que existem
    coluna_ordem = [col for col in coluna_ordem if col in pivot_data.columns]
    pivot_data = pivot_data[coluna_ordem]
    
    # Ordenar por região e município
    pivot_data = pivot_data.sort_values(['regiao', 'municipio']).reset_index(drop=True)
    
    print(f"💾 Salvando dados harmonizados em {output_csv}...")
    pivot_data.to_csv(output_csv, index=False, encoding='utf-8-sig')
    
    print(f"✅ Harmonização concluída!")
    print(f"   - {len(pivot_data)} registros")
    print(f"   - {len(pivot_data.columns)} colunas")
    
    return pivot_data


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    input_file = base_dir / "dados_climatologicos_processados.csv"
    output_file = base_dir / "dados_climatologicos_harmonizados.csv"
    
    if input_file.exists():
        harmonizar_dados(str(input_file), str(output_file))
    else:
        print(f"❌ Arquivo de entrada não encontrado: {input_file}")
