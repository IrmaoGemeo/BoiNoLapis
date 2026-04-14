import streamlit as st
import pandas as pd

st.set_page_config(page_title="Boi no Lápis", layout="wide")

st.title("📊 Boi no Lápis: Gestão e Gráficos")

col1, col2 = st.columns(2)

with col1:
    st.header("Dados do Lote")
    valor_bezerro = st.number_input("Preço de compra do animal (R$)", 0.0)
    custos_fixos = st.number_input("Custos de manejo e ração (R$)", 0.0)
    peso_abate = st.number_input("Peso de abate (KG)", 0.0)
    cotacao_venda = st.number_input("Preço da @ de venda (R$)", 0.0)

with col2:
    st.header("Painel de Resultados")
    
    total_arrobas = peso_abate / 30
    investimento = valor_bezerro + custos_fixos
    faturamento = total_arrobas * cotacao_venda
    lucro_liquido = faturamento - investimento
    
    if total_arrobas > 0:
        st.metric("Lucro Final", f"R$ {lucro_liquido:,.2f}")
        st.metric("Ponto de Equilíbrio (@)", f"R$ {investimento/total_arrobas:,.2f}")
        
        # Preparação do gráfico comparativo
        df = pd.DataFrame({
            "Financeiro": ["Investimento", "Faturamento"],
            "Valores (R$)": [investimento, faturamento]
        })
        
        st.bar_chart(df.set_index("Financeiro"))
    else:
        st.info("Preencha os campos para visualizar indicadores financeiros.")
