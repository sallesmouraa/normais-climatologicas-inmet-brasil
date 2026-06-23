# Guia de Harmonização de Dados

## O que foi mudado?

Este repositório foi atualizado para resolver dois problemas críticos:

### 1. ✅ Git LFS Configurado
- `.gitattributes` agora rastreia arquivos CSV com Git LFS
- O arquivo `dados_climatologicos_processados.csv` (16 MB) será eficientemente versionado
- Clones serão muito mais rápidos

### 2. ✅ Formato de Dados Harmonizado
- **Antes**: Formato "longo" (uma linha por variável/mês/estação)
- **Depois**: Formato "largo" consolidado (uma linha por município com agregações anuais)

## Novo Formato de Dados

O arquivo `dados_climatologicos_harmonizados.csv` contém:

| Coluna | Descrição | Tipo |
|--------|-----------|------|
| `codigo_estacao` | ID único da estação INMET | string |
| `municipio` | Nome do município | string |
| `estado` | Sigla do estado (SP, RJ, etc) | string |
| `regiao` | Região do Brasil (Norte, Nordeste, etc) | string |
| `latitude` | Latitude do município | float |
| `longitude` | Longitude do município | float |
| `temperatura_media` | Temperatura média anual (°C) | float |
| `temperatura_maxima` | Temperatura máxima anual (°C) | float |
| `temperatura_minima` | Temperatura mínima anual (°C) | float |
| `precipitacao_media` | Precipitação média anual (mm) | float |
| `umidade_relativa` | Umidade relativa média anual (%) | float |

## Como Usar

### Passo 1: Gerar dados harmonizados
```bash
python harmonizar_dados.py
```
Isso transforma `dados_climatologicos_processados.csv` em `dados_climatologicos_harmonizados.csv`.

### Passo 2: Rodar a API (FastAPI)
```bash
make dev
# ou
python -m uvicorn api_normais_climatologicas_do_brasil:app --reload --host 0.0.0.0 --port 8000
```

**Novos endpoints da API:**
- `GET /clima` — Todos os dados consolidados
- `GET /clima/{municipio_id}` — Dados de um município (por código ou nome)
- `GET /clima/search?municipio=...&estado=...&regiao=...` — Busca com filtros
- `GET /regioes` — Lista de regiões
- `GET /estados` — Lista de estados
- `GET /municipios?estado=SP` — Lista de municípios (com filtro opcional)
- `GET /estatisticas?estado=SP` — Estatísticas agregadas

### Passo 3: Rodar o Dashboard (Streamlit)
```bash
streamlit run app.py
```

Ou com variável de ambiente customizada:
```bash
DATA_FILE_PATH=dados_climatologicos_harmonizados.csv streamlit run app.py
```

## Arquivos Modificados

### 📝 Novos Arquivos
- **`harmonizar_dados.py`** — Script para transformar dados brutos em formato consolidado
- **`.gitattributes`** — Configuração do Git LFS

### 🔄 Arquivos Atualizados
- **`api_normais_climatologicas_do_brasil.py`** — Atualizada para usar dados harmonizados
- **`app.py`** — Dashboard Streamlit atualizado, corrigido o bug de session_state
- **`README.md`** (próxima etapa) — Será atualizado com informações corretas

## Fluxo de Dados Completo

```
dados_climatologicos_processados.csv (16 MB, formato longo)
                ↓
         harmonizar_dados.py
                ↓
dados_climatologicos_harmonizados.csv (formato largo consolidado)
                ↓
         ┌──────────────────┬──────────────────┐
         ↓                  ↓
    API FastAPI        Dashboard Streamlit
  (api_*.py)              (app.py)
```

## Checklist de Implementação

- [x] Configurar Git LFS (`.gitattributes`)
- [x] Criar script de harmonização (`harmonizar_dados.py`)
- [x] Atualizar API para novo formato
- [x] Atualizar Dashboard para novo formato
- [x] Corrigir bug do `st.session_state`
- [ ] Atualizar README principal com informações corretas
- [ ] Publicar no PyPI (próxima etapa)

## Próximos Passos

1. Executar `python harmonizar_dados.py` uma vez para gerar os dados harmonizados
2. Testar a API com `make dev`
3. Testar o Dashboard com `streamlit run app.py`
4. Atualizar o README principal
5. (Opcional) Adicionar latitude/longitude real via geolocalização

## Suporte

Para dúvidas ou problemas:
- 📖 [GitHub Issues](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil/issues)
- 💬 [GitHub Discussions](https://github.com/sallesmouraa/normais-climatologicas-inmet-brasil/discussions)
