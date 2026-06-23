# 🌍 Normais Climatológicas Brasil (1991-2020)

[![Python](https://img.shields.io/badge/python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPL--3.0-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![GitHub stars](https://img.shields.io/github/stars/sallesmouraa/normais-climatologicas-inmet-brasil?style=flat-square)](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil)

Repositório de dados estruturados e API em Python para consulta das **Normais Climatológicas do Brasil**, utilizando a base de dados oficial do **INMET** e **INPE**.

Uma solução completa para análise de dados climáticos históricos do Brasil (1991-2020), com **API REST (FastAPI)** e **Dashboard Interativo (Streamlit)**, desenvolvida para integração com o ecossistema **GeoSense AI**.

---

## 🎯 Objetivo

Este projeto facilita o acesso a médias históricas consolidadas de temperatura, precipitação e umidade por município brasileiro, servindo de base para:

- 📋 **Laudos Ambientais**: Comparação de dados atuais com a média histórica de 30 anos
- 🗺️ **Análise Geográfica**: Estudo de variabilidade climática regional e por bioma
- 🌾 **Agro de Precisão**: Planejamento agrícola baseado em ciclos de chuva históricos
- 🔬 **Pesquisa Científica**: Base confiável para estudos climáticos e ambientais

---

## 📊 Dados Utilizados

| Aspecto | Detalhes |
|--------|----------|
| **Fonte** | Instituto Nacional de Meteorologia (INMET) & INPE |
| **Período** | 1991 a 2020 (30 anos de histórico) |
| **Cobertura** | Todos os municípios brasileiros |
| **Formato** | CSV consolidado por município (uma linha por município) |
| **Tamanho** | ~16 MB (rastreado com Git LFS) |

---

## 🚀 Início Rápido

### Setup Automático (Recomendado)
```bash
# Clone o repositório
git clone https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil.git
cd normais-climatologicas-inmet-brasil

# Setup completo (instala deps, cria .env, harmoniza dados)
make setup
```

### Rodar a API (FastAPI)
```bash
make dev
```
Acesse: http://localhost:8000/docs (Swagger UI interativa)

### Rodar o Dashboard (Streamlit)
```bash
make dashboard
```
Acesse: http://localhost:8501

---

## 📖 Como Usar

### 1️⃣ Uso Básico (Python)

```python
import pandas as pd

# Carregar dados harmonizados
dados = pd.read_csv('dados_climatologicos_harmonizados.csv')

# Ver primeiras linhas
print(dados.head())
```

### 2️⃣ Filtrar por Município

```python
# Obter dados do Rio de Janeiro
rio = dados[dados['municipio'].str.contains('Rio de Janeiro', case=False)]
print(rio[['municipio', 'estado', 'temperatura_media', 'precipitacao_media']])
```

### 3️⃣ Filtrar por Estado

```python
# Obter dados de São Paulo
sp = dados[dados['estado'] == 'SP']
print(f"Temperatura média em SP: {sp['temperatura_media'].mean():.2f}°C")
print(f"Precipitação média em SP: {sp['precipitacao_media'].mean():.0f}mm")
```

### 4️⃣ Análise Geográfica por Região

```python
# Clima por região
regiao_stats = dados.groupby('regiao')[['temperatura_media', 'precipitacao_media']].mean()
print(regiao_stats)

# Município mais quente
mais_quente = dados.loc[dados['temperatura_media'].idxmax()]
print(f"Município mais quente: {mais_quente['municipio']} ({mais_quente['temperatura_media']:.1f}°C)")
```

### 5️⃣ Usar a API REST

```bash
# Todos os dados
curl http://localhost:8000/clima

# Dados de um município
curl http://localhost:8000/clima/rio%20de%20janeiro

# Busca por filtros
curl "http://localhost:8000/clima/search?estado=SP&regiao=Sudeste"

# Estatísticas por estado
curl "http://localhost:8000/estatisticas?estado=SP"

# Listar regiões
curl http://localhost:8000/regioes

# Listar municípios de um estado
curl "http://localhost:8000/municipios?estado=SP"
```

---

## 📁 Estrutura do Projeto

```
normais-climatologicas-inmet-brasil/
├── 📄 README.md                              # Este arquivo
├── 📄 LICENSE                                # Licença GPL-3.0
├── 📄 HARMONIZACAO.md                        # Guia de harmonização de dados
├── 📄 MUDANCAS.md                            # Resumo das mudanças recentes
├── 📄 CONTRIBUTING.md                        # Guia de contribuição
├── 📄 requirements.txt                       # Dependências Python
├── 📄 setup.py                               # Configuração para PyPI
├── 📄 pyproject.toml                         # Config moderna (PEP 517)
├── 📄 Makefile                               # Automação de tarefas
├── 📄 .gitattributes                         # Configuração Git LFS
├── 📊 dados_climatologicos_processados.csv   # Base bruta (Git LFS, 16 MB)
├── 📊 dados_climatologicos_harmonizados.csv  # Base consolidada (gerada)
├── 🐍 api_normais_climatologicas_do_brasil.py # API FastAPI
├── 🐍 app.py                                 # Dashboard Streamlit
├── 🐍 harmonizar_dados.py                    # Script de harmonização
├── 📝 .env.example                           # Variáveis de ambiente (exemplo)
└── 🔧 .gitignore                             # Arquivos ignorados pelo Git
```

---

## 📊 Estrutura dos Dados

O arquivo `dados_climatologicos_harmonizados.csv` contém uma linha por município com:

| Coluna | Descrição | Tipo | Intervalo |
|--------|-----------|------|-----------|
| `codigo_estacao` | ID único da estação INMET | string | ex: "83000" |
| `municipio` | Nome do município | string | ex: "Rio de Janeiro" |
| `estado` | Sigla do estado | string | SP, RJ, MG, ... |
| `regiao` | Região geográfica | string | Norte, Nordeste, Centro-Oeste, Sudeste, Sul |
| `latitude` | Latitude do município | float | -33.77 a 5.27 |
| `longitude` | Longitude do município | float | -73.98 a -34.79 |
| `temperatura_media` | Temperatura média anual (°C) | float | 15.5 a 28.5 |
| `temperatura_maxima` | Temperatura máxima anual (°C) | float | 20.0 a 35.0 |
| `temperatura_minima` | Temperatura mínima anual (°C) | float | 10.0 a 25.0 |
| `precipitacao_media` | Precipitação média anual (mm) | float | 500 a 3000 |
| `umidade_relativa` | Umidade relativa média (%) | float | 60 a 85 |

---

## 🌐 Cobertura Geográfica

- ✅ **27 Unidades Federativas** (26 estados + DF)
- ✅ **240+ Municípios com dados INMET**
- ✅ **5 Regiões**: Norte, Nordeste, Centro-Oeste, Sudeste, Sul
- ✅ **Todos os Biomas**: Amazônia, Cerrado, Caatinga, Mata Atlântica, Pantanal, Pampas

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** — Linguagem principal
- **FastAPI** — Framework para API REST de alto desempenho
- **Streamlit** — Framework para dashboard interativo
- **Pandas** — Manipulação e análise de dados
- **NumPy** — Computação numérica
- **Plotly** — Visualizações interativas
- **Git LFS** — Versionamento eficiente de arquivos grandes

---

## 📋 Dependências

### Básicas
```
fastapi>=0.111,<1.0
uvicorn[standard]>=0.30,<1.0
pandas>=2.2,<3.0
numpy>=1.21.0
```

### Dashboard
```
streamlit>=1.0
plotly>=5.0
```

---

## 📈 Roadmap

- [x] Publicar dados climatológicos iniciais
- [x] Criar API básica de consulta
- [x] Documentação inicial
- [x] API REST (FastAPI) com múltiplos endpoints
- [x] Dashboard Streamlit interativo
- [x] Harmonização de dados (formato consolidado)
- [x] Git LFS para eficiência de repositório
- [ ] Publicar no PyPI
- [ ] Adicionar testes automatizados
- [ ] Criar CLI interativa
- [ ] Atualização automática de dados
- [ ] Suporte a dados geoespaciais (GeoPandas)
- [ ] Geocodificação de latitude/longitude precisa

---

## 🤝 Como Contribuir

Contribuições são bem-vindas! Para contribuir:

1. **Fork** este repositório
2. **Crie uma branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra um Pull Request**

Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes sobre padrões de código e processo de contribuição.

---

## 📝 Licença

Este projeto está licenciado sob a **GNU General Public License v3.0** - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Rodrigo Salles** ([@sallesmouraa](https://github.com/sallesmouraa))

- 🌐 Estudante de Geografia 
- 🗺️ Especialista em Geospatial & GeoAI
- 📊 Data Science & Climate Analysis

---

## 📞 Suporte

- 📖 [Documentação - Harmonização](HARMONIZACAO.md)
- 📋 [Registro de Mudanças](MUDANCAS.md)
- 🐛 [Reportar bugs](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil/issues)
- 💬 [Discussões](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil/discussions)

---

## 🙏 Agradecimentos

- **INMET** — Instituto Nacional de Meteorologia pelos dados brutos
- **INPE** — Instituto Nacional de Pesquisas Espaciais
- **GeoSense AI** — Pelo suporte ao projeto
- **Comunidade open source Python** — Pelos excelentes libraries

---

## 📚 Referências

- [INMET - Instituto Nacional de Meteorologia](https://www.inmet.gov.br/)
- [INPE - Instituto Nacional de Pesquisas Espaciais](https://www.inpe.br/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NumPy Documentation](https://numpy.org/)

---

**⭐ Se este projeto foi útil para você, considere deixar uma estrela!**

Desenvolvido com ❤️ para a comunidade geoespacial brasileira.
