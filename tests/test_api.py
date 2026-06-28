"""Tests for the FastAPI application."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from api_normais_climatologicas_do_brasil import app


@pytest.fixture
def client():
    """FastAPI test client."""
    return TestClient(app)


class TestRootEndpoint:
    """Test root endpoint."""

    def test_read_root(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data
        assert data["message"] == "Bem-vindo à API de Normais Climatológicas do Brasil"


class TestMetadataEndpoints:
    """Test metadata endpoints."""

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_get_regioes(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/regioes")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "Nordeste" in data
        assert "Sudeste" in data

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_get_estados(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/estados")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "SP" in data
        assert "RJ" in data
        assert "BA" in data

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_get_municipios(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/municipios")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "SAO PAULO" in data
        assert "RIO DE JANEIRO" in data
        assert "SALVADOR" in data

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_get_municipios_por_estado(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/municipios?estado=SP")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "SAO PAULO" in data
        assert "RIO DE JANEIRO" not in data


class TestClimaEndpoints:
    """Test climate data endpoints."""

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_get_clima_by_municipio_found(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/clima/SAO PAULO")
        assert response.status_code == 200
        data = response.json()
        assert data["municipio"] == "SAO PAULO"
        assert data["estado"] == "SP"
        assert data["temperatura_media"] == 19.5

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_get_clima_by_municipio_not_found(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/clima/INEXISTENTE")
        assert response.status_code == 404
        assert "detail" in response.json()

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_search_clima_por_estado(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/clima/search?estado=SP")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["estado"] == "SP"

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_search_clima_sem_resultados(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/clima/search?estado=XX")
        assert response.status_code == 404
        assert "detail" in response.json()

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_search_clima_por_municipio(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/clima/search?municipio=rio")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "RIO" in data[0]["municipio"]


class TestEstatisticasEndpoint:
    """Test statistics endpoint."""

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_get_estatisticas(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/estatisticas")
        assert response.status_code == 200
        data = response.json()
        assert "total_municipios" in data
        assert "temperatura_media" in data
        assert "precipitacao_media" in data
        assert "umidade_relativa" in data
        assert "minimo" in data["temperatura_media"]
        assert "maximo" in data["temperatura_media"]
        assert "media" in data["temperatura_media"]
        assert data["total_municipios"] == 3
        assert isinstance(data["temperatura_media"]["media"], float)

    @patch("api_normais_climatologicas_do_brasil.get_dataframe")
    def test_get_estatisticas_por_estado(self, mock_get_dataframe, client, mock_dataframe):
        mock_get_dataframe.return_value = mock_dataframe
        response = client.get("/estatisticas?estado=SP")
        assert response.status_code == 200
        data = response.json()
        assert data["total_municipios"] == 1
        assert data["temperatura_media"]["media"] == 19.5
