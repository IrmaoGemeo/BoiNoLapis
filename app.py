import streamlit as st
import pandas as pd
import altair as alt

# Configuração da página
st.set_page_config(page_title="Boi no Lápis", layout="wide")

# Estilização visual customizada
st.markdown("""
    <style>
    .stApp {
        background-color: #121212;
        color: #ffffff;
    }
    
    [data-testid="stVerticalBlock"] > div:has(div.element-container) {
        background-color: #1e1e1e;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #333;
    }

    .stNumberInput div[data-baseweb="input"] {
        background-color: #262626;
        border-radius: 8px;
        color: white;
    }

    h1, h2, h3 {
        color: #e0e0e0 !important;
    }
    
    .badge-lucro {
        background-color: #2e7d32;
        color: #a5d6a7;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        float: right;
    }
    
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
    
    # Cálculo das arrobas limpas conforme padrão técnico
    total_arrobas = (peso_abate * (rendimento / 100)) / 15
    st.markdown(f"### Arrobas do lote \n ## {total_arrobas:.1f} @")

with col_res:
    investimento = valor_bezerro + custos_fixos
    faturamento = total_arrobas * cotacao_venda
    lucro_liquido = faturamento - investimento
    
    # Define o status do badge
    status = "lucrativo" if lucro_liquido > 0 else "prejuízo"
    cor_badge = "#2e7d32" if lucro_liquido > 0 else "#c62828"
    
    st.markdown(f'<span class="badge-lucro" style="background-color: {cor_badge};">{status}</span>', unsafe_allow_html=True)
    st.subheader("PAINEL DE RESULTADOS")
    
    margem = (lucro_liquido / faturamento) * 100 if faturamento > 0 else 0
    ponto_equilibrio = investimento / total_arrobas if total_arrobas > 0 else 0
    resultado_arroba = lucro_liquido / total_arrobas if total_arrobas > 0 else 0

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

    # Gráfico Altair para evitar erro de cores
    df_grafico = pd.DataFrame({
        "Categoria": ["Faturamento", "Investimento", "Lucro"],
        "Valores": [faturamento, investimento, lucro_liquido]
    })
    
    chart = alt.Chart(df_grafico).mark_bar().encode(
        x=alt.X("Categoria", sort=None, title=None),
        y=alt.Y("Valores", title="Valor (R$)"),
        color=alt.Color("Categoria", scale=alt.Scale(
            domain=["Faturamento", "Investimento", "Lucro"],
            range=["#2e7d32", "#d84315", "#2e7d32"]
        ), legend=None)
    ).properties(height=350)
    
    st.altair_chart(chart, use_container_width=True)
    
    st.info(f"Dica: seu equilíbrio é R$ {ponto_equilibrio:.2f}/@. Você vende a R$ {cotacao_venda:.2f}/@.")
