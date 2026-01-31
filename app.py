"""
Billboard Hot 100 - Consulta de Charts Históricos
Aplicação Streamlit para busca de músicas da Billboard com integração Spotify
"""
import streamlit as st
from datetime import datetime
from services.billboard_service import BillboardService
from services.spotify_service import SpotifyService
from utils.helpers import validate_date, format_chart_date, format_display_date


# Configuração da página
st.set_page_config(
    page_title="Billboard Hot 100 Explorer",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .rank-badge {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1DB954;
    }
    .stats-badge {
        font-size: 0.85rem;
        color: #666;
        padding: 2px 6px;
        background: #f0f0f0;
        border-radius: 4px;
        margin-right: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa o dataset
with st.spinner("🔄 Carregando dataset..."):
    if not BillboardService.initialize_dataset():
        st.error("❌ Erro ao carregar o dataset. Verifique a instalação.")
        st.stop()

# Cabeçalho
st.markdown('<div class="main-title">🎵 Billboard Hot 100 Explorer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Explore o histórico da Billboard de 1958 a Maio/2021</div>', unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📅 Selecione a Data")

# Obter range de anos disponíveis
min_year, max_year = BillboardService.get_available_date_range()

# Seletores de data
col1, col2 = st.sidebar.columns(2)

with col1:
    selected_month = st.selectbox(
        "Mês",
        range(1, 13),
        index=0,  # Janeiro por padrão
        format_func=lambda x: [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ][x - 1]
    )

with col2:
    selected_year = st.selectbox(
        "Ano",
        range(max_year, min_year - 1, -1),
        index=1  # 2020 por padrão
    )

# Botão de busca
search_button = st.sidebar.button("🔍 Buscar Chart", type="primary", use_container_width=True)

# Informações na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Sobre")
st.sidebar.info(
    f"Este aplicativo consulta o histórico da **Billboard Hot 100** "
    f"usando um dataset do Kaggle.\n\n"
    f"📊 Dados de **Agosto/1958** até **Maio/2021**\n\n"
    f"🎧 Links diretos para o Spotify"
)

st.sidebar.markdown("### 📊 Dataset")
st.sidebar.caption("Fonte: Kaggle - Billboard Hot 100 Audio Features by Sean Miller")

# Área principal
if search_button:
    # Validar data
    is_valid, error_msg = validate_date(selected_year, selected_month)
    
    if not is_valid:
        st.error(f"❌ {error_msg}")
    else:
        # Formatar data
        date_str = format_chart_date(selected_year, selected_month)
        display_date = format_display_date(selected_year, selected_month)
        
        # Buscar chart
        with st.spinner(f"🔎 Buscando chart de {display_date}..."):
            chart = BillboardService.get_chart(date_str)
        
        if chart:
            # Cabeçalho dos resultados
            st.success(f"✅ Chart de **{display_date}** carregado com sucesso!")
            st.markdown(f"### 🏆 Top 100 - {display_date}")
            st.markdown(f"*Total de músicas: {len(chart)}*")
            st.markdown("---")
            
            # Exibir todas as músicas
            for song in chart:
                col1, col2, col3 = st.columns([0.5, 3.5, 1])
                
                with col1:
                    st.markdown(f'<div class="rank-badge">#{song["rank"]}</div>', unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**{song['title']}**")
                    
                    # Informações do artista e estatísticas
                    stats_html = f"🎤 {song['artist']}"
                    
                    if song['weeks_on_chart'] and song['weeks_on_chart'] > 0:
                        stats_html += f" • <span class='stats-badge'>📅 {song['weeks_on_chart']} semanas</span>"
                    
                    if song['peak_pos'] and song['peak_pos'] > 0:
                        stats_html += f" • <span class='stats-badge'>🏆 Pico: #{song['peak_pos']}</span>"
                    
                    if song['last_week'] and song['last_week'] > 0:
                        diff = song['last_week'] - song['rank']
                        if diff > 0:
                            stats_html += f" • <span class='stats-badge'>📈 +{diff}</span>"
                        elif diff < 0:
                            stats_html += f" • <span class='stats-badge'>📉 {diff}</span>"
                    
                    if song['isNew']:
                        stats_html += f" • <span class='stats-badge'>🆕 NOVA</span>"
                    
                    st.markdown(stats_html, unsafe_allow_html=True)
                
                with col3:
                    spotify_url = SpotifyService.generate_search_url(
                        song['title'], 
                        song['artist']
                    )
                    st.link_button(
                        "🎧 Spotify",
                        spotify_url,
                        use_container_width=True
                    )
                
                st.markdown("---")
        
        else:
            st.error(
                f"❌ Não foi possível carregar o chart de {display_date}.\n\n"
                f"O dataset contém dados de **Agosto/1958** a **Maio/2021**. "
                "Tente selecionar uma data dentro deste período."
            )

else:
    # Tela inicial
    st.info("👈 Selecione uma data na barra lateral e clique em **Buscar Chart** para começar!")
    
    # Exemplos
    st.markdown("### 💡 Exemplos de Consultas Populares")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🎤 2021")
        st.markdown("Experimente: **Janeiro de 2021**")
    
    with col2:
        st.markdown("#### 🎸 Anos 2000")
        st.markdown("Experimente: **Janeiro de 2000**")
    
    with col3:
        st.markdown("#### 📻 Década de 80")
        st.markdown("Experimente: **Julho de 1985**")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666;'>"
    "Desenvolvido com ❤️ usando Streamlit | Dataset: Kaggle | Música: Spotify"
    "</div>",
    unsafe_allow_html=True
)