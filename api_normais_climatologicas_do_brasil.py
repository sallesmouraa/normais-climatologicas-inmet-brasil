# -*- coding: utf-8 -*-
"""API de Normais Climatológicas do Brasil.

Script enxuto para:
1. carregar e padronizar arquivos CSV de normais climatológicas;
2. salvar um CSV consolidado;
3. expor os dados via FastAPI.

O código foi reescrito para remover dependências de Google Colab,
comandos mágicos de notebook e blocos de texto narrativos misturados ao código.
"""

from __future__ import annotations

from pathlib import Path
import re
import unicodedata
from typing import Iterable

import pandas as pd
from fastapi import FastAPI, HTTPException, Query


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_FILE = BASE_DIR / "dados_climatologicos_processados.csv"

MONTH_TO_NUM = {
    "janeiro": 1,
    "fevereiro": 2,
    "marco": 3,
    "abril": 4,
    "maio": 5,
    "junho": 6,
    "julho": 7,
    "agosto": 8,
    "setembro": 9,
    "outubro": 10,
    "novembro": 11,
    "dezembro": 12,
}


def remove_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(char for char in normalized if not unicodedata.combining(char))


def normalize_text(value: str) -> str:
    value = remove_accents(str(value)).strip().lower()
    value = re.sub(r"\s+", "_", value)
    value = re.sub(r"[^a-z0-9_]", "", value)
    return value


def extract_variable_name(filename: str) -> str:
    stem = Path(filename).stem
    cleaned = re.sub(
        r"\s*NCB_\d{4}-\d{4}|\s*\(\d+\)|Alt-\d{2}-\d{2}-\d{4}|_\d{4}-\d{4}",
        "",
        stem,
        flags=re.IGNORECASE,
    )
    cleaned = cleaned.replace("-", " ").replace("_", " ").strip()
    return " ".join(word.capitalize() for word in cleaned.split())


def find_header_index(lines: Iterable[str]) -> int:
    for index, line in enumerate(lines):
        normalized = normalize_text(line)
        if "codigo" in normalized and "janeiro" in normalized:
            return index
    return 0


def clean_column_name(column: str) -> str:
    normalized = normalize_text(column)
    mapping = {
        "codigo": "codigo_estacao",
        "codigo_estacao": "codigo_estacao",
        "nome": "nome_estacao",
        "nome_da_estacao": "nome_estacao",
        "estacao": "nome_estacao",
        "uf": "uf",
    }
    return mapping.get(normalized, normalized)


def parse_numeric_series(series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        series.astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
        errors="coerce",
    )


def load_csv_file(csv_path: Path) -> pd.DataFrame:
    with csv_path.open("r", encoding="latin-1", errors="ignore") as file:
        preview_lines = [file.readline() for _ in range(15)]

    header_index = find_header_index(preview_lines)
    df = pd.read_csv(csv_path, sep=";", encoding="latin-1", header=header_index)
    df.columns = [clean_column_name(col) for col in df.columns]
    df = df.loc[:, ~df.columns.duplicated()]
    df = df.dropna(axis=1, how="all")

    required_columns = {"codigo_estacao", "nome_estacao"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Arquivo {csv_path.name} não possui colunas obrigatórias: {sorted(required_columns)}"
        )

    if "uf" not in df.columns:
        df["uf"] = pd.NA

    month_columns = [column for column in df.columns if column in MONTH_TO_NUM]
    if not month_columns:
        raise ValueError(f"Arquivo {csv_path.name} não possui colunas mensais válidas")

    df = df.dropna(subset=["codigo_estacao", "nome_estacao"])
    df["codigo_estacao"] = df["codigo_estacao"].astype(str).str.strip()
    df["nome_estacao"] = df["nome_estacao"].astype(str).str.strip()
    df["uf"] = df["uf"].astype(str).str.strip()

    melted = df.melt(
        id_vars=["codigo_estacao", "nome_estacao", "uf"],
        value_vars=month_columns,
        var_name="mes_nome",
        value_name="valor_variavel",
    )
    melted["mes"] = melted["mes_nome"].map(MONTH_TO_NUM)
    melted["valor_variavel"] = parse_numeric_series(melted["valor_variavel"])
    melted["variavel_climatica"] = extract_variable_name(csv_path.name)
    melted = melted.dropna(subset=["mes", "valor_variavel"])

    return melted[
        ["codigo_estacao", "nome_estacao", "uf", "variavel_climatica", "mes", "valor_variavel"]
    ]


def build_dataset(data_dir: Path = DATA_DIR, output_file: Path = OUTPUT_FILE) -> pd.DataFrame:
    csv_files = sorted(data_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Nenhum arquivo CSV encontrado em: {data_dir}")

    frames: list[pd.DataFrame] = []
    errors: list[str] = []

    for csv_file in csv_files:
        if csv_file.name == output_file.name:
            continue
        try:
            frames.append(load_csv_file(csv_file))
        except Exception as exc:
            errors.append(f"{csv_file.name}: {exc}")

    if not frames:
        raise ValueError("Nenhum arquivo CSV válido foi processado. Erros: " + " | ".join(errors))

    complete_df = pd.concat(frames, ignore_index=True)
    complete_df.to_csv(output_file, index=False, encoding="utf-8-sig")
    return complete_df


def load_processed_data(csv_path: Path = OUTPUT_FILE) -> pd.DataFrame:
    if not csv_path.exists():
        return build_dataset()

    df = pd.read_csv(csv_path)
    df["codigo_estacao"] = df["codigo_estacao"].astype(str)
    if "mes" in df.columns:
        df["mes"] = pd.to_numeric(df["mes"], errors="coerce").astype("Int64")
    if "valor_variavel" in df.columns:
        df["valor_variavel"] = pd.to_numeric(df["valor_variavel"], errors="coerce")
    return df


app = FastAPI(
    title="API de Normais Climatológicas do Brasil",
    description="API para servir dados climatológicos processados do Brasil.",
    version="1.0.0",
)


def get_dataframe() -> pd.DataFrame:
    return load_processed_data()


@app.get("/", tags=["Root"])
def read_root() -> dict[str, str]:
    return {"message": "Bem-vindo à API de Normais Climatológicas do Brasil"}


@app.get("/clima", tags=["Dados Climatológicos"])
def get_all_clima_data() -> list[dict]:
    df = get_dataframe()
    return df.to_dict(orient="records")


@app.get("/clima/{station_id}", tags=["Dados Climatológicos"])
def get_clima_by_station_id(station_id: str) -> list[dict]:
    df = get_dataframe()
    station_data = df[df["codigo_estacao"] == str(station_id)].to_dict(orient="records")
    if not station_data:
        raise HTTPException(status_code=404, detail=f"Estação com ID '{station_id}' não encontrada")
    return station_data


@app.get("/clima/search", tags=["Dados Climatológicos"])
def search_clima_data(
    nome_estacao: str | None = Query(default=None, description="Filtrar por nome da estação"),
    mes: int | None = Query(default=None, description="Filtrar por mês (1-12)"),
    variavel_climatica: str | None = Query(default=None, description="Filtrar por variável climática"),
    uf: str | None = Query(default=None, description="Filtrar por UF"),
) -> list[dict]:
    df = get_dataframe().copy()

    if nome_estacao:
        df = df[df["nome_estacao"].str.contains(nome_estacao, case=False, na=False)]

    if uf:
        df = df[df["uf"].str.upper() == uf.upper()]

    if variavel_climatica:
        df = df[
            df["variavel_climatica"].str.contains(variavel_climatica, case=False, na=False)
        ]

    if mes is not None:
        if not 1 <= mes <= 12:
            raise HTTPException(status_code=400, detail="Mês deve ser um valor entre 1 e 12")
        df = df[df["mes"] == mes]

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado para os critérios informados")

    return df.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
