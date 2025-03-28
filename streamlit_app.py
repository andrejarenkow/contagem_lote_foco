import streamlit as st
import pandas as pd
import re

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
    
    return df

st.title("Processador de Arquivo de Texto")

uploaded_file = st.file_uploader("Faça o upload do arquivo .txt", type=["txt"])

codigo_evento = st.text_input("Digite o código do evento:")

if uploaded_file and codigo_evento:
    df_resultante = process_file(uploaded_file, codigo_evento)
    
    if df_resultante is not None and not df_resultante.empty:
        st.write("### Dados filtrados:")
        st.dataframe(df_resultante)
    else:
        st.warning("Nenhum dado encontrado para o código informado.")
