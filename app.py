# Painel de Vendas - kit de reserva da Aula 2 (Geração de Código)
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Painel de Vendas", layout="wide")
st.title("Painel de Vendas")

# Leitura dos dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("vendas.csv", parse_dates=["data"])
    df["mes"] = df["data"].dt.to_period("M").astype(str)
    return df

df = carregar_dados()

# Filtros na barra lateral
st.sidebar.header("Filtros")
produtos = st.sidebar.multiselect("Produto", sorted(df["produto"].unique()), default=sorted(df["produto"].unique()))
regioes = st.sidebar.multiselect("Região", sorted(df["regiao"].unique()), default=sorted(df["regiao"].unique()))
filtrado = df[df["produto"].isin(produtos) & df["regiao"].isin(regioes)]

# Indicadores
faturamento = filtrado["valor"].sum()
quantidade = int(filtrado["quantidade"].sum())
ticket = faturamento / len(filtrado) if len(filtrado) else 0
c1, c2, c3 = st.columns(3)
c1.metric("Faturamento", f"R$ {faturamento:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c2.metric("Quantidade vendida", quantidade)
c3.metric("Ticket médio", f"R$ {ticket:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

# Gráfico de faturamento por mês
st.subheader("Faturamento por mês")
st.bar_chart(filtrado.groupby("mes")["valor"].sum())

# Tabela filtrada
st.subheader("Vendas")
st.dataframe(filtrado.drop(columns="mes"))
