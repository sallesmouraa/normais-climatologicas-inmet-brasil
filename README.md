# 🌍 Normais Climatológicas Brasil (1991-2020)

[![Python](https://img.shields.io/badge/python-3.8+-blue?style=flat-square&logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-GPL--3.0-green?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-brightgreen?style=flat-square)](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square)](https://github.com/psf/black)
[![GitHub stars](https://img.shields.io/github/stars/sallesmouraa/normais-climatologicas-inmet-brasil?style=flat-square)](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil/stargazers)

Repositório de dados estruturados e API em Python para consulta das **Normais Climatológicas do Brasil**, utilizando a base de dados oficial do **INMET** e **INPE**.

Uma solução completa para análise de dados climáticos históricos do Brasil (1991-2020), desenvolvida para integração com o ecossistema **GeoSense AI**.

---

## 🎯 Objetivo

Este projeto foi desenvolvido para facilitar o acesso a médias históricas de temperatura e precipitação por município brasileiro, servindo de base para:

- 📋 **Laudos Ambientais**: Comparação de dados atuais com a média histórica de 30 anos
- 🗺️ **Análise Geográfica**: Estudo de variabilidade climática regional e por bioma
- 🌾 **Agro de Precisão**: Planejamento agrícola baseado em ciclos de chuva históricos
- 🔬 **Pesquisa Científica**: Base confiável para estudos climáticos e ambientais

---

## 📊 Dados Utilizados

| Aspecto | Detalhes |
|--------|----------|
| **Fonte** | Instituto Nacional de Meteorologia (INMET) & INPE |
| **Período** | 1991 a 2020 (Base mais recente - 30 anos) |
| **Cobertura** | Todos os municípios brasileiros |
| **Formato** | CSV estruturado processado em Python |
| **Tamanho** | ~16 MB de dados estruturados |

---

## 🚀 Instalação

### Via pip (em breve no PyPI)

```bash
pip install normais-climatologicas-inmet
```

### Instalação Local para Desenvolvimento

```bash
# Clone o repositório
git clone https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil.git
cd normais-climatologicas-inmet-brasil

# Instale as dependências
pip install -r requirements.txt

# Ou com setup.py
pip install -e .
```

### Dependências

- **Python** 3.8+
- **pandas** >= 1.3.0
- **numpy** >= 1.21.0

---

## 📖 Como Usar

### 1️⃣ Uso Básico

```python
import pandas as pd
from api_normais_climatologicas_do_brasil import consultar_dados

# Carregar todos os dados
dados = pd.read_csv('dados_climatologicos_processados.csv')

# Ver primeiras linhas
print(dados.head())
```

### 2️⃣ Filtrar por Município

```python
# Obter dados do Rio de Janeiro
rio = dados[dados['municipio'].str.contains('Rio de Janeiro', case=False)]
print(rio[['municipio', 'temperatura_media', 'precipitacao_media']])
```

### 3️⃣ Filtrar por Estado

```python
# Obter dados de São Paulo
sp = dados[dados['estado'] == 'SP']
print(f"Temperaturas médias em SP: {sp['temperatura_media'].mean():.2f}°C")
```

### 4️⃣ Análise de Clima por Região

```python
# Média de chuva por região
regiao = dados.groupby('regiao')['precipitacao_media'].mean()
print(regiao)

# Município mais quente
mais_quente = dados.loc[dados['temperatura_media'].idxmax()]
print(f"Município mais quente: {mais_quente['municipio']}")
```

---

## 📁 Estrutura do Projeto

```
normais-climatologicas-inmet-brasil/
├── 📄 README.md                              # Este arquivo
├── 📄 LICENSE                                # Licença GPL-3.0
├── 📄 requirements.txt                       # Dependências Python
├── 📄 setup.py                               # Configuração para PyPI
├── 📄 pyproject.toml                         # Config moderna (PEP 517)
├── 📄 Makefile                               # Automação de tarefas
├── 📊 dados_climatologicos_processados.csv   # Base de dados (16 MB)
├── 🐍 api_normais_climatologicas_do_brasil.py # API principal
├── 📝 .env.example                           # Variáveis de exemplo
└── 🔧 .gitignore                             # Arquivos ignorados pelo Git
```

---

## 📊 Estrutura dos Dados

O arquivo CSV contém as seguintes colunas principais:

| Coluna | Descrição | Tipo |
|--------|-----------|------|
| `municipio` | Nome do município | string |
| `estado` | Sigla do estado (SP, RJ, MG, etc) | string |
| `regiao` | Região do Brasil (Norte, Nordeste, etc) | string |
| `latitude` | Latitude do município | float |
| `longitude` | Longitude do município | float |
| `temperatura_media` | Temperatura média (°C) | float |
| `temperatura_maxima` | Temperatura máxima (°C) | float |
| `temperatura_minima` | Temperatura mínima (°C) | float |
| `precipitacao_media` | Precipitação média (mm) | float |
| `umidade_relativa` | Umidade relativa do ar (%) | float |

---

## 🌐 Cobertura Geográfica

- ✅ **27 Unidades Federativas** (26 estados + DF)
- ✅ **240+ Municípios brasileiros**
- ✅ **5 Regiões**: Norte, Nordeste, Centro-Oeste, Sudeste, Sul
- ✅ **Todos os Biomas**: Amazônia, Cerrado, Caatinga, Mata Atlântica, Pantanal, Pampas

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+** - Linguagem principal
- **Pandas** - Manipulação e análise de dados
- **NumPy** - Computação numérica
- **Git** - Controle de versão
- **GitHub Actions** - CI/CD (em breve)

---

## 📈 Roadmap

- [x] Publicar dados climatológicos iniciais
- [x] Criar API básica de consulta
- [x] Documentação inicial
- [ ] Publicar no PyPI
- [ ] Adicionar testes automatizados
- [ ] Criar CLI interativa
- [ ] Adicionar Dashboard Streamlit
- [ ] API REST (FastAPI)
- [ ] Atualização automática de dados
- [ ] Suporte a dados geoespaciais (GeoPandas)

---

## 🤝 Como Contribuir

Contribuições são bem-vindas! Para contribuir:

1. **Fork** este repositório
2. **Crie uma branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. **Abra um Pull Request**

Por favor, leia [CONTRIBUTING.md](CONTRIBUTING.md) para mais detalhes.

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

- 📖 Documentação: [GitHub Wiki](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil/wiki)
- 🐛 Reportar bugs: [Issues](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil/issues)
- 💬 Discussões: [GitHub Discussions](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil/discussions)

---

## 🙏 Agradecimentos

- **INMET** - Instituto Nacional de Meteorologia pelos dados brutos
- **INPE** - Instituto Nacional de Pesquisas Espaciais
- **GeoSense AI** - Pelo suporte ao projeto
- Comunidade open source Python

---

## 📚 Referências

- [INMET - Instituto Nacional de Meteorologia](https://www.inmet.gov.br/)
- [INPE - Instituto Nacional de Pesquisas Espaciais](https://www.inpe.br/)
- [Pandas Documentation](https://pandas.pydata.org/)
- [NumPy Documentation](https://numpy.org/)

---

**⭐ Se este projeto foi útil para você, considere deixar uma estrela!**

Desenvolvido com ❤️ para a comunidade geoespacial brasileira.
