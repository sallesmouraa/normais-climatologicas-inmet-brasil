"""Tests for the Streamlit app functions."""

import sys
from unittest.mock import MagicMock

# Mock streamlit before importing app to avoid UI execution during tests
mock_st = MagicMock()
mock_st.cache_data = lambda **kwargs: (lambda f: f)
sys.modules["streamlit"] = mock_st

import pandas as pd
import pytest

from app import carregar_dados


class TestCarregarDados:
    """Test data loading functions."""

    def test_carregar_dados_arquivo_nao_encontrado(self):
        """Test carregar_dados returns None when file not found."""
        result = carregar_dados("/caminho/inexistente/dados.csv")
        assert result is None

    def test_carregar_dados_colunas_faltando(self, tmp_path):
        """Test carregar_dados raises ValueError when required columns are missing."""
        csv_file = tmp_path / "dados_incompleto.csv"
        df = pd.DataFrame({
            "regiao": ["Sudeste"],
            "estado": ["SP"],
        })
        df.to_csv(csv_file, index=False)

        with pytest.raises(ValueError, match="Colunas obrigatórias ausentes"):
            carregar_dados(str(csv_file))

    def test_carregar_dados_valido(self, tmp_path):
        """Test carregar_dados loads valid CSV correctly."""
        csv_file = tmp_path / "dados_valido.csv"
        df = pd.DataFrame({
            "regiao": ["Sudeste", "Nordeste"],
            "estado": ["SP", "BA"],
            "municipio": ["SAO PAULO", "SALVADOR"],
            "temperatura_media": [19.5, 25.5],
            "temperatura_maxima": [25.0, 31.0],
            "precipitacao_media": [120.0, 2000.0],
            "umidade_relativa": [75.0, 85.0],
        })
        df.to_csv(csv_file, index=False)

        result = carregar_dados(str(csv_file))

        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "municipio" in result.columns
        assert result["municipio"].tolist() == ["SAO PAULO", "SALVADOR"]

    def test_carregar_dados_arquivo_vazio(self, tmp_path):
        """Test carregar_dados returns None for empty file."""
        csv_file = tmp_path / "dados_vazio.csv"
        csv_file.write_text("")

        result = carregar_dados(str(csv_file))
        assert result is None
