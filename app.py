import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Normais Climatológicas Brasil",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <h1 style='text-align: center; color: #1f77b4;'>
        🌍 Normais Climatológicas Brasil (1991-2020)
    </h1>
    <p style='text-align: center; color: #666;'>
        Dashboard Interativo | INMET/INPE
    </p>
""",
    unsafe_allow_html=True,
)

st.divider()

# Usar arquivo harmonizado por padrão
DATA_FILE_PATH = Path(os.getenv("DATA_FILE_PATH", "dados_climatologicos_harmonizados.csv"))
REQUIRED_COLUMNS = {
    "regiao",
    "estado",
    "municipio",
    "temperatura_media",
    "temperatura_maxima",
    "precipitacao_media",
    "umidade_relativa",
}


@st.cache_data(show_spinner=False)
def carregar_dados(data_file_path: str) -> pd.DataFrame | None:
    try:
        df = pd.read_csv(data_file_path)
    except FileNotFoundError:
        return None
    except pd.errors.EmptyDataError:
        return None
    except pd.errors.ParserError:
        return None

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {sorted(missing)}")

    return df


def filtrar_dados(df: pd.DataFrame) -> tuple[pd.DataFrame, str]:
    """Aplica filtros e retorna dados filtrados + região selecionada."""
    st.sidebar.title("🔍 Filtros")
    st.sidebar.divider()

    regioes = ["Todas"] + sorted(df["regiao"].dropna().astype(str).unique().tolist())
    regiao = st.sidebar.selectbox("Região:", regioes)
    dados_filtrados = df.copy()
    if regiao != "Todas":
        dados_filtrados = dados_filtrados[dados_filtrados["regiao"] == regiao].copy()

    estados = ["Todos"] + sorted(dados_filtrados["estado"].dropna().astype(str).unique().tolist())
    estado = st.sidebar.selectbox("Estado:", estados)
    if estado != "Todos":
        dados_filtrados = dados_filtrados[dados_filtrados["estado"] == estado].copy()

    municipios = ["Todos"] + sorted(
        dados_filtrados["municipio"].dropna().astype(str).unique().tolist()
    )
    municipio = st.sidebar.selectbox("Município:", municipios)
    if municipio != "Todos":
        dados_filtrados = dados_filtrados[dados_filtrados["municipio"] == municipio].copy()

    st.sidebar.divider()
    st.sidebar.info(f"📊 {len(dados_filtrados)} registros")
    
    return dados_filtrados, regiao


def mostrar_metricas(df: pd.DataFrame) -> None:
    st.subheader("📊 Estatísticas")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌡️ Temp. Média", f"{df['temperatura_media'].mean():.1f}°C")
    with col2:
        st.metric("🔥 Temp. Máxima", f"{df['temperatura_maxima'].mean():.1f}°C")
    with col3:
        st.metric("💧 Precipitação", f"{df['precipitacao_media'].mean():.0f}mm")
    with col4:
        st.metric("💨 Umidade", f"{df['umidade_relativa'].mean():.1f}%")


def mostrar_graficos(df: pd.DataFrame, regiao_selecionada: str) -> None:
    st.subheader("📈 Visualizações")
    tab1, tab2, tab3 = st.tabs(["Temperatura", "Precipitação", "Comparação"])

    with tab1:
        if len(df) <= 20:
            fig1 = px.bar(
                df.sort_values("temperatura_media", ascending=False),
                x="municipio",
                y="temperatura_media",
                title="Temperatura Média",
                color="temperatura_media",
                color_continuous_scale="Reds",
            )
            st.plotly_chart(fig1, use_container_width=True)
        else:
            st.info("Refine os filtros para visualizar os gráficos por município.")

    with tab2:
        if len(df) <= 20:
            fig2 = px.bar(
                df.sort_values("precipitacao_media", ascending=False),
                x="municipio",
                y="precipitacao_media",
                title="Precipitação Média",
                color="precipitacao_media",
                color_continuous_scale="Blues",
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Refine os filtros para visualizar os gráficos por município.")

    with tab3:
        if regiao_selecionada == "Todas":
            df_r = (
                df.groupby("regiao", as_index=False)[["temperatura_media", "precipitacao_media"]]
                .mean()
            )
            fig3 = px.bar(
                df_r,
                x="regiao",
                y="temperatura_media",
                title="Temperatura por Região",
                color="temperatura_media",
                color_continuous_scale="Reds",
            )
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("A comparação por região aparece quando o filtro de região está em 'Todas'.")


def main() -> None:
    try:
        dados = carregar_dados(str(DATA_FILE_PATH))
    except ValueError as exc:
        st.error(f"❌ Arquivo de dados inválido: {exc}")
        st.stop()

    if dados is None:
        st.error(
            f"❌ Arquivo '{DATA_FILE_PATH}' não encontrado ou não pôde ser lido.\n\n"
            "Verifique a variável de ambiente `DATA_FILE_PATH`."
        )
        st.stop()

    dados_filtrados, regiao_selecionada = filtrar_dados(dados)

    if dados_filtrados.empty:
        st.warning("Nenhum dado encontrado para os filtros selecionados.")
        st.stop()

    mostrar_metricas(dados_filtrados)
    st.divider()
    mostrar_graficos(dados_filtrados, regiao_selecionada)
    st.divider()

    st.subheader("📋 Dados")
    linhas = st.slider("Linhas:", 1, max(len(dados_filtrados), 1), min(10, len(dados_filtrados)))
    st.dataframe(dados_filtrados.head(linhas), use_container_width=True)

    st.divider()
    st.subheader("📥 Download")
    col1, col2 = st.columns(2)

    with col1:
        csv = dados_filtrados.to_csv(index=False)
        st.download_button("📥 CSV", csv, "dados.csv", "text/csv", use_container_width=True)

    with col2:
        json_data = dados_filtrados.to_json(orient="records")
        st.download_button(
            "📥 JSON",
            json_data,
            "dados.json",
            "application/json",
            use_container_width=True,
        )

    st.divider()
    st.markdown(
        "<p style='text-align: center; color: #666;'>🌍 Desenvolvido com ❤️ | Rodrigo Salles</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
