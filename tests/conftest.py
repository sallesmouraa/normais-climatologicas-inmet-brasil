"""Pytest configuration and shared fixtures."""

import pandas as pd
import pytest


@pytest.fixture
def mock_dataframe():
    """Returns a mock DataFrame for testing."""
    return pd.DataFrame([
        {
            "codigo_estacao": "A701",
            "municipio": "SAO PAULO",
            "estado": "SP",
            "regiao": "Sudeste",
            "temperatura_media": 19.5,
            "temperatura_maxima": 25.0,
            "temperatura_minima": 14.0,
            "precipitacao_media": 120.0,
            "umidade_relativa": 75.0,
            "latitude": -23.5,
            "longitude": -46.6,
        },
        {
            "codigo_estacao": "A801",
            "municipio": "RIO DE JANEIRO",
            "estado": "RJ",
            "regiao": "Sudeste",
            "temperatura_media": 24.0,
            "temperatura_maxima": 30.0,
            "temperatura_minima": 18.0,
            "precipitacao_media": 150.0,
            "umidade_relativa": 80.0,
            "latitude": -22.9,
            "longitude": -43.1,
        },
        {
            "codigo_estacao": "A901",
            "municipio": "SALVADOR",
            "estado": "BA",
            "regiao": "Nordeste",
            "temperatura_media": 25.5,
            "temperatura_maxima": 31.0,
            "temperatura_minima": 20.0,
            "precipitacao_media": 2000.0,
            "umidade_relativa": 85.0,
            "latitude": -12.9,
            "longitude": -38.5,
        },
    ])
