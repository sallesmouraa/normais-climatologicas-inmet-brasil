import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# Configuração da página
st.set_page_config(
    page_title="Normais Climatológicas Brasil",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <h1 style='text-align: center; color: #1f77b4;'>
        🌍 Normais Climatológicas Brasil (1991-2020)
    </h1>
    <p style='text-align: center; color: #666;'>
        Dashboard Interativo | INMET/INPE
    </p>
""", unsafe_allow_html=True)

st.divider()

# Carregando dados
@st.cache_data
def carregar_dados():
    try:
        df = pd.read_csv('dados_climatologicos_processados.csv')
        return df
    except:
        return None

dados = carregar_dados()

if dados is not None:
    # SIDEBAR - FILTROS
    st.sidebar.title("🔍 Filtros")
    st.sidebar.divider()
    
    regioes = ['Todas'] + sorted(dados['regiao'].unique().tolist())
    regiao = st.sidebar.selectbox('Região:', regioes)
    
    if regiao != 'Todas':
        dados_f = dados[dados['regiao'] == regiao].copy()
    else:
        dados_f = dados.copy()
    
    estados = ['Todos'] + sorted(dados_f['estado'].unique().tolist())
    estado = st.sidebar.selectbox('Estado:', estados)
    
    if estado != 'Todos':
        dados_f = dados_f[dados_f['estado'] == estado].copy()
    
    municipios = ['Todos'] + sorted(dados_f['municipio'].unique().tolist())
    municipio = st.sidebar.selectbox('Município:', municipios)
    
    if municipio != 'Todos':
        dados_f = dados_f[dados_f['municipio'] == municipio].copy()
    
    st.sidebar.divider()
    st.sidebar.info(f"📊 {len(dados_f)} registros")
    
    # ESTATÍSTICAS
    st.subheader("📊 Estatísticas")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("🌡️ Temp. Média", f"{dados_f['temperatura_media'].mean():.1f}°C")
    with col2:
        st.metric("🔥 Temp. Máxima", f"{dados_f['temperatura_maxima'].mean():.1f}°C")
    with col3:
        st.metric("💧 Precipitação", f"{dados_f['precipitacao_media'].mean():.0f}mm")
    with col4:
        st.metric("💨 Umidade", f"{dados_f['umidade_relativa'].mean():.1f}%")
    
    st.divider()
    
    # GRÁFICOS
    st.subheader("📈 Visualizações")
    tab1, tab2, tab3 = st.tabs(["Temperatura", "Precipitação", "Comparação"])
    
    with tab1:
        if len(dados_f) <= 20:
            fig1 = px.bar(dados_f.sort_values('temperatura_media', ascending=False),
                         x='municipio', y='temperatura_media', title='Temperatura Média',
                         color='temperatura_media', color_continuous_scale='Reds')
            st.plotly_chart(fig1, use_container_width=True)
    
    with tab2:
        if len(dados_f) <= 20:
            fig2 = px.bar(dados_f.sort_values('precipitacao_media', ascending=False),
                         x='municipio', y='precipitacao_media', title='Precipitação Média',
                         color='precipitacao_media', color_continuous_scale='Blues')
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab3:
        if regiao == 'Todas':
            df_r = dados.groupby('regiao')[['temperatura_media', 'precipitacao_media']].mean().reset_index()
            fig3 = px.bar(df_r, x='regiao', y='temperatura_media', title='Temperatura por Região',
                         color='temperatura_media', color_continuous_scale='Reds')
            st.plotly_chart(fig3, use_container_width=True)
    
    st.divider()
    
    # TABELA
    st.subheader("📋 Dados")
    linhas = st.slider('Linhas:', 1, len(dados_f), 10)
    st.dataframe(dados_f.head(linhas), use_container_width=True)
    
    st.divider()
    
    # DOWNLOAD
    st.subheader("📥 Download")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = dados_f.to_csv(index=False)
        st.download_button("📥 CSV", csv, "dados.csv", "text/csv", use_container_width=True)
    
    with col2:
        json_data = dados_f.to_json(orient='records')
        st.download_button("📥 JSON", json_data, "dados.json", "application/json", use_container_width=True)
    
    st.divider()
    st.markdown("<p style='text-align: center; color: #666;'>🌍 Desenvolvido com ❤️ | Rodrigo Salles</p>", unsafe_allow_html=True)

else:
    st.error("❌ Arquivo 'dados_climatologicos_processados.csv' não encontrado!")
