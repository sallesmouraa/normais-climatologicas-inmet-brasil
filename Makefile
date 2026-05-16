.PHONY: help install dev prod lint format test clean docker-build docker-up docker-down docker-logs env-setup serve

# ========================================
# Variáveis
# ========================================
PYTHON := python3
PIP := pip3
VENV := venv
DOCKER_IMAGE := normais-climatologicas:latest
DOCKER_CONTAINER := normais-api

# ========================================
# Help - Exibe todos os comandos disponíveis
# ========================================
help:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║   Normais Climatológicas Brasil - Makefile                ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "📦 INSTALAÇÃO:"
	@echo "  make install          - Instala dependências"
	@echo "  make env-setup        - Cria .env do .env.example"
	@echo ""
	@echo "🚀 DESENVOLVIMENTO:"
	@echo "  make dev              - Roda API em modo desenvolvimento"
	@echo "  make serve            - Alias para 'make dev'"
	@echo "  make prod             - Roda API em modo produção"
	@echo ""
	@echo "🔍 QUALIDADE DE CÓDIGO:"
	@echo "  make lint             - Verifica código com flake8"
	@echo "  make format           - Formata código com black"
	@echo "  make test             - Roda testes com pytest"
	@echo ""
	@echo "🐳 DOCKER:"
	@echo "  make docker-build     - Constrói imagem Docker"
	@echo "  make docker-up        - Inicia container Docker"
	@echo "  make docker-down      - Para container Docker"
	@echo "  make docker-logs      - Exibe logs do container"
	@echo ""
	@echo "🧹 LIMPEZA:"
	@echo "  make clean            - Remove arquivos temporários"
	@echo "  make clean-all        - Remove venv e todos os cache"
	@echo ""

# ========================================
# Instalação
# ========================================
install:
	@echo "📦 Instalando dependências..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✅ Dependências instaladas com sucesso!"

install-dev:
	@echo "📦 Instalando dependências + dev tools..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install pytest pytest-cov black flake8 mypy
	@echo "✅ Dependências e ferramentas de desenvolvimento instaladas!"

# ========================================
# Configuração do Ambiente
# ========================================
env-setup:
	@if [ -f .env ]; then \
		echo "⚠️  .env já existe. Use 'make env-reset' para recriar."; \
	else \
		cp .env.example .env; \
		echo "✅ .env criado a partir de .env.example"; \
		echo "📝 Edite o arquivo .env para configurar suas variáveis"; \
	fi

env-reset:
	@echo "🔄 Recriando .env..."
	@cp .env.example .env
	@echo "✅ .env recriado com valores padrão"

# ========================================
# Desenvolvimento
# ========================================
dev:
	@echo "🚀 Iniciando API em modo DESENVOLVIMENTO..."
	@echo "📍 Acesse: http://localhost:8000"
	@echo "📚 Documentação: http://localhost:8000/docs"
	@echo "🛑 Pressione Ctrl+C para parar"
	$(PYTHON) -m uvicorn api_normais_climatologicas_do_brasil:app --reload --host 0.0.0.0 --port 8000

serve: dev

prod:
	@echo "🚀 Iniciando API em modo PRODUÇÃO..."
	@echo "📍 Acesse: http://0.0.0.0:8000"
	$(PYTHON) -m uvicorn api_normais_climatologicas_do_brasil:app --host 0.0.0.0 --port 8000 --workers 4

# ========================================
# Qualidade de Código
# ========================================
lint:
	@echo "🔍 Verificando código com flake8..."
	@$(PYTHON) -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "✅ Verificação concluída!"

format:
	@echo "🎨 Formatando código com black..."
	@$(PYTHON) -m black . --line-length 100
	@echo "✅ Código formatado!"

test:
	@echo "🧪 Rodando testes com pytest..."
	@$(PYTHON) -m pytest -v --cov=. --cov-report=html
	@echo "✅ Testes concluídos! Veja o relatório em htmlcov/index.html"

test-quick:
	@echo "⚡ Rodando testes rapidamente..."
	@$(PYTHON) -m pytest -v --tb=short
	@echo "✅ Testes concluídos!"

# ========================================
# Docker
# ========================================
docker-build:
	@echo "🐳 Construindo imagem Docker..."
	@docker build -t $(DOCKER_IMAGE) .
	@echo "✅ Imagem construída com sucesso!"

docker-up:
	@echo "🚀 Iniciando container Docker..."
	@docker-compose up -d
	@echo "✅ Container iniciado!"
	@echo "📍 Acesse: http://localhost:8000"
	@docker ps -f name=$(DOCKER_CONTAINER)

docker-down:
	@echo "🛑 Parando container Docker..."
	@docker-compose down
	@echo "✅ Container parado!"

docker-logs:
	@echo "📋 Logs do container:"
	@docker logs -f $(DOCKER_CONTAINER)

docker-clean:
	@echo "🧹 Removendo container e volumes..."
	@docker-compose down -v
	@echo "✅ Container e volumes removidos!"

# ========================================
# Limpeza
# ========================================
clean:
	@echo "🧹 Limpando arquivos temporários..."
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".coverage" -delete 2>/dev/null || true
	@find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Limpeza concluída!"

clean-all: clean
	@echo "🗑️  Removendo venv e dependências..."
	@rm -rf $(VENV)
	@echo "✅ Limpeza completa concluída!"

# ========================================
# Utilitários
# ========================================
check-deps:
	@echo "📋 Verificando dependências instaladas..."
	@$(PIP) list | grep -E "fastapi|uvicorn|pandas|pydantic"

check-python:
	@echo "🐍 Versão do Python:"
	@$(PYTHON) --version
	@echo "📦 Versão do pip:"
	@$(PIP) --version

info:
	@echo "╔════════════════════════════════════════════════════════════╗"
	@echo "║   Informações do Projeto                                  ║"
	@echo "╚════════════════════════════════════════════════════════════╝"
	@make check-python
	@echo ""
	@make check-deps

# ========================================
# Setup Inicial
# ========================================
setup: install env-setup info
	@echo ""
	@echo "✅ Setup concluído! Próximos passos:"
	@echo "1. Edite .env com suas configurações"
	@echo "2. Execute 'make dev' para iniciar a API"
	@echo "3. Acesse http://localhost:8000/docs"

# ========================================
# Default
# ========================================
.DEFAULT_GOAL := help
