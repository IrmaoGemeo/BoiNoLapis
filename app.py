import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Boi no Lápis", layout="wide")

# CSS para customização visual
st.markdown("""
    <style>
    /* Fundo principal */
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    
    /* Estilização dos containers (Cards) */
    [data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #333;
    }

    /* Estilização de inputs */
    .stNumberInput div[data-baseweb="input"] {
        background-color: #262626;
        border-radius: 8px;
        color: white;
    }

    /* Customização dos textos */
    h1, h2, h3 {
        color: #e0e0e0 !important;
    }
    
    /* Badge Lucrativo */
    .badge-lucro {
        background-color: #2e7d32;
        color: #a5d6a7;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        float: right;
    }
    
    /* Blocos de métricas customizados */
    .metric-card {
        background-color: #262626;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 10px;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #9e9e9e;
        margin-bottom: 5px;
    }
    .metric-value {
        font-size: 1.2rem;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Boi no Lápis: Gestão e Gráficos")

col_dados, col_res = st.columns([1, 1.2], gap="large")

with col_dados:
    st.subheader("DADOS DO LOTE")
    valor_bezerro = st.number_input("Preço de compra do animal (R$)", value=2500.0)
    custos_fixos = st.number_input("Custos de manejo e ração (R$)", value=1200.0)
    peso_abate = st.number_input("Peso de abate (kg)", value=540.0)
    rendimento = st.slider("Rendimento de Carcaça (%)", 40, 60, 52)
    cotacao_venda = st.number_input("Preço da @ de venda (R$)", value=230.0)
    
    total_arrobas = (peso_abate * (rendimento / 100)) / 15
    st.markdown(f"### Arrobas do lote \n ## {total_arrobas:.1f} @")

with col_res:
    st.markdown('<span class="badge-lucro">lucrativo</span>', unsafe_allow_html=True)
    st.subheader("PAINEL DE RESULTADOS")
    
    investimento = valor_bezerro + custos_fixos
    faturamento = total_arrobas * cotacao_venda
    lucro_liquido = faturamento - investimento
    margem = (lucro_liquido / faturamento) * 100 if faturamento > 0 else 0
    ponto_equilibrio = investimento / total_arrobas if total_arrobas > 0 else 0
    resultado_arroba = lucro_liquido / total_arrobas if total_arrobas > 0 else 0

    # Grid de métricas estilo o print
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Faturamento</div><div class="metric-value" style="color: #4caf50;">R$ {faturamento:,.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><div class="metric-label">Ponto de equilíbrio</div><div class="metric-value" style="color: #ffb300;">R$ {ponto_equilibrio:,.2f}</div></div>', unsafe_allow_html=True)
    
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Investimento</div><div class="metric-value" style="color: #ff7043;">R$ {investimento:,.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><div class="metric-label">Margem de lucro</div><div class="metric-value" style="color: #8bc34a;">{margem:.1f} %</div></div>', unsafe_allow_html=True)
        
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-label">Lucro final</div><div class="metric-value" style="color: #4caf50;">R$ {lucro_liquido:,.2f}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-card"><div class="metric-label">Resultado/@</div><div class="metric-value" style="color: #8bc34a;">R$ {resultado_arroba:,.2f}/@</div></div>', unsafe_allow_html=True)

    # Gráfico com cores customizadas
    df_grafico = pd.DataFrame({
        "Categoria": ["Faturamento", "Investimento", "Lucro"],
        "Valores": [faturamento, investimento, lucro_liquido]
    })
    
    st.bar_chart(df_grafico.set_index("Categoria"), color=["#2e7d32", "#d84315", "#2e7d32"])
    
    st.info(f"Dica: seu equilíbrio é R$ {ponto_equilibrio:.2f}/@. Você vende a R$ {cotacao_venda:.2f}/@.")
