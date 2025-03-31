import streamlit as st
import pandas as pd
import re
import plotly.express as px

# Configurações da página
st.set_page_config(
    page_title="Contagem lote",
    page_icon=":camera:",
    #layout="wide",
    initial_sidebar_state='collapsed'
) 

def process_text(text, codigo_evento, codigo_fotografo):
    linhas = text.split("\n")  # Separar por linhas
    
    dados = []
    padrao = re.compile(r"(\d+)\s+([\w\s]+ \d+ Pixels)\s+(\w+\d+)")
    
    for linha in linhas:
        match = padrao.search(linha)
        if match:
            dados.append(match.groups())
    
    if not dados:
        return None  # Retorna None se nenhum dado for encontrado
    
    df = pd.DataFrame(dados, columns=["Número de Pedidos", "Resolução", "Cód."])
    df = df[df["Cód."].str.startswith(f"{codigo_fotografo}{codigo_evento}")].reset_index(drop=True)
    # Extrair o número logo após "LENS{codigo_evento}" como o Lote
    df["Lote"] = df["Cód."].str[len(f"LENS{codigo_evento}")].astype(str)
    df["Número de Pedidos"] = df["Número de Pedidos"].astype(int)
    
    return df

st.title("Processador de Texto")

text_input = st.text_area("Cole ou digite o conteúdo do arquivo:")
codigo_fotografo = st.text_input("Digite a sigla do fotógrafo:")
codigo_evento = st.text_input("Digite o código do evento:")

if text_input and codigo_evento:
    df_resultante = process_text(text_input, codigo_evento, codigo_fotografo)
    
    if df_resultante is not None and not df_resultante.empty:

        # Mostrando um card de total de vendas
        total_vendas = len(df_resultante)

        st.metric(value = total_vendas, label = f'Total de vendas do evento {codigo_evento}')
        
        # Criar gráfico
        st.write("### Distribuição de fotos por lote")
        df_resultante['Lote'] = df_resultante['Lote'].astype(str)
        contagem_por_lote = df_resultante.groupby("Lote")["Número de Pedidos"].count().reset_index()
        
        fig = px.bar(contagem_por_lote, x="Lote", y="Número de Pedidos", title="Número de Pedidos por Lote", color="Lote", text="Número de Pedidos")
        fig.update_traces(textposition='outside')

        # Mostrando o gráfico
        st.plotly_chart(fig)

        # Mostrando tabela de venda por lote
        st.write("### Vendas por lote:")
        st.dataframe(contagem_por_lote, hide_index=True)

        # Mostrando tabela bruta
        st.write("### Tabela bruta:")
        st.dataframe(contagem_por_lote, hide_index=True)
    else:
        st.warning("Nenhum dado encontrado para o código informado.")
