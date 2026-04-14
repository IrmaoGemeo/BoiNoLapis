import streamlit as st

st.title("Calculadora de Lucro na Pecuária")

valor_compra = st.number_input("Valor de compra do animal (R$)", value=0.0)
custo_nutricao = st.number_input("Gasto total com ração (R$)", value=0.0)
peso_final_kg = st.number_input("Peso final em KG", value=0.0)
preco_venda_arroba = st.number_input("Preço de venda da arroba (R$)", value=0.0)

arrobas = peso_final_kg / 30
custo_total = valor_compra + custo_nutricao
receita_total = arrobas * preco_venda_arroba
lucro_final = receita_total - custo_total

if arrobas > 0:
    st.write(f"Custo por arroba: R$ {custo_total / arrobas:.2f}")
    st.write(f"Lucro final por animal: R$ {lucro_final:.2f}")