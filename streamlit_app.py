import streamlit as st
import pandas as pd
import re
import plotly.express as px

def process_file(file, codigo_evento):
    linhas = file.readlines()
    linhas = [linha.decode("utf-8") for linha in linhas]  # Decodificar para string
    
    dados = []
    padrao = re.compile(r"(\d+)\s+([\w\s]+ \d+ Pixels)\s+(\w+\d+)")
    
    for linha in linhas:
        match = padrao.search(linha)
        if match:
            dados.append(match.groups())
    
    if not dados:
        return None  # Retorna None se nenhum dado for encontrado
    
    df = pd.DataFrame(dados, columns=["Número de Pedidos", "Resolução", "Cód."])
    df = df[df["Cód."].str.startswith(f"LENS{codigo_evento}")].reset_index(drop=True)
    df["Lote"] = df["Cód."].str[10]
    df["Número de Pedidos"] = df["Número de Pedidos"].astype(int)
    
    return df

st.title("Processador de Arquivo de Texto")

uploaded_file = st.file_uploader("Faça o upload do arquivo .txt", type=["txt"])

codigo_evento = st.text_input("Digite o código do evento:")

if uploaded_file and codigo_evento:
    df_resultante = process_file(uploaded_file, codigo_evento)
    
    if df_resultante is not None and not df_resultante.empty:

        # Criar gráfico
        st.write("### Distribuição de fotos por lote")
        contagem_por_lote = df_resultante.groupby("Lote")["Número de Pedidos"].sum().reset_index()
        
        fig = px.bar(contagem_por_lote, x="Lote", y="Número de Pedidos", title="Número de Pedidos por Lote", color="Lote")
        
        st.plotly_chart(fig)

        st.write("### Tabela bruta:")
        st.dataframe(df_resultante)
    else:
        st.warning("Nenhum dado encontrado para o código informado.")
