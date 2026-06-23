# -*- coding: utf-8 -*-
"""API de Normais Climatológicas do Brasil.

API FastAPI para servir dados consolidados de normais climatológicas
agrupados por município/estado.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd
from fastapi import FastAPI, HTTPException, Query


BASE_DIR = Path(__file__).resolve().parent
HARMONIZED_DATA_FILE = BASE_DIR / "dados_climatologicos_harmonizados.csv"

app = FastAPI(
    title="API de Normais Climatológicas do Brasil",
    description="API para servir dados climatológicos processados e consolidados do Brasil por município.",
    version="2.0.0",
)


def load_processed_data(csv_path: Path = HARMONIZED_DATA_FILE) -> pd.DataFrame:
    """Carrega dados climatológicos harmonizados."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Arquivo de dados não encontrado: {csv_path}\n"
            "Execute 'python harmonizar_dados.py' para gerar o arquivo."
        )
    
    df = pd.read_csv(csv_path)
    
    # Conversão de tipos
    df["codigo_estacao"] = df["codigo_estacao"].astype(str)
    
    numeric_cols = [
        "temperatura_media", "temperatura_maxima", "temperatura_minima",
        "precipitacao_media", "umidade_relativa", "latitude", "longitude"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    
    return df


def get_dataframe() -> pd.DataFrame:
    """Retorna DataFrame dos dados climatológicos."""
    return load_processed_data()


@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    """Raiz da API."""
    return {
        "message": "Bem-vindo à API de Normais Climatológicas do Brasil",
        "version": "2.0.0",
        "docs": "/docs"
    }


@app.get("/clima", tags=["Dados Climatológicos"])
def get_all_clima_data() -> list[dict]:
    """Retorna todos os dados climatológicos consolidados."""
    df = get_dataframe()
    return df.to_dict(orient="records")


@app.get("/clima/{municipio_id}", tags=["Dados Climatológicos"])
def get_clima_by_municipio(municipio_id: str) -> dict:
    """Retorna dados climatológicos de um município específico."""
    df = get_dataframe()
    
    # Buscar por código ou nome
    municipio_data = df[
        (df["codigo_estacao"] == municipio_id) | 
        (df["municipio"].str.lower() == municipio_id.lower())
    ]
    
    if municipio_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"Município '{municipio_id}' não encontrado"
        )
    
    return municipio_data.iloc[0].to_dict()


@app.get("/clima/search", tags=["Dados Climatológicos"])
def search_clima_data(
    municipio: Optional[str] = Query(None, description="Filtrar por nome do município"),
    estado: Optional[str] = Query(None, description="Filtrar por estado (ex: SP, RJ)"),
    regiao: Optional[str] = Query(None, description="Filtrar por região (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)"),
) -> list[dict]:
    """Busca dados climatológicos com filtros."""
    df = get_dataframe().copy()
    
    if municipio:
        df = df[df["municipio"].str.contains(municipio, case=False, na=False)]
    
    if estado:
        df = df[df["estado"].str.upper() == estado.upper()]
    
    if regiao:
        df = df[df["regiao"].str.contains(regiao, case=False, na=False)]
    
    if df.empty:
        raise HTTPException(
            status_code=404,
            detail="Nenhum dado encontrado para os critérios informados"
        )
    
    return df.to_dict(orient="records")


@app.get("/regioes", tags=["Metadados"])
def get_regioes() -> list[str]:
    """Retorna lista de regiões disponíveis."""
    df = get_dataframe()
    return sorted(df["regiao"].dropna().unique().tolist())


@app.get("/estados", tags=["Metadados"])
def get_estados() -> list[str]:
    """Retorna lista de estados disponíveis."""
    df = get_dataframe()
    return sorted(df["estado"].dropna().unique().tolist())


@app.get("/municipios", tags=["Metadados"])
def get_municipios(
    estado: Optional[str] = Query(None, description="Filtrar municípios por estado")
) -> list[str]:
    """Retorna lista de municípios disponíveis."""
    df = get_dataframe()
    
    if estado:
        df = df[df["estado"].str.upper() == estado.upper()]
    
    return sorted(df["municipio"].dropna().unique().tolist())


@app.get("/estatisticas", tags=["Análises"])
def get_estatisticas(
    estado: Optional[str] = Query(None, description="Filtrar por estado")
) -> dict:
    """Retorna estatísticas agregadas dos dados climatológicos."""
    df = get_dataframe()
    
    if estado:
        df = df[df["estado"].str.upper() == estado.upper()]
    
    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
    
    return {
        "total_municipios": len(df),
        "temperatura_media": {
            "minimo": float(df["temperatura_media"].min()),
            "maximo": float(df["temperatura_media"].max()),
            "media": float(df["temperatura_media"].mean()),
        },
        "precipitacao_media": {
            "minimo": float(df["precipitacao_media"].min()),
            "maximo": float(df["precipitacao_media"].max()),
            "media": float(df["precipitacao_media"].mean()),
        },
        "umidade_relativa": {
            "minimo": float(df["umidade_relativa"].min()),
            "maximo": float(df["umidade_relativa"].max()),
            "media": float(df["umidade_relativa"].mean()),
        },
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
