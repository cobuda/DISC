import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuração da página
st.set_page_config(page_title="Portal DISC - Time", layout="wide")

# Nome do arquivo de banco de dados simples
DB_FILE = "dados_disc.csv"

# Inicializar banco de dados se não existir
if not os.path.exists(DB_FILE):
    df_init = pd.DataFrame(columns=['Nome', 'Data', 'D', 'I', 'S', 'C'])
    df_init.to_csv(DB_FILE, index=False)

def carregar_dados():
    return pd.read_csv(DB_FILE)

# --- INTERFACE ---
st.title("📊 Sistema de Avaliação DISC")

aba_form, aba_dashboard = st.tabs(["Responder Formulário", "Análise do Time"])

# --- ABA 1: FORMULÁRIO ---
with aba_form:
    st.header("Formulário de Autoavaliação")
    st.write("Responda de 0 a 10 o quanto você se identifica com cada pilar:")
    
    with st.form("disc_form"):
        nome = st.selectbox("Selecione seu nome", ["Ana", "Bruno", "Caio", "Duda", "Enzo", "Fernanda", "Guto", "Helô", "Igor", "Julia"])
        data = st.date_input("Data da avaliação")
        
        col1, col2 = st.columns(2)
        with col1:
            d = st.slider("Dominância (D): Firme, decidido, focado em resultados?", 0, 10, 5)
            i = st.slider("Influência (I): Comunicativo, entusiasmado, persuasivo?", 0, 10, 5)
        with col2:
            s = st.slider("Estabilidade (S): Paciente, bom ouvinte, metódico?", 0, 10, 5)
            c = st.slider("Conformidade (C): Analítico, detalhista, preciso?", 0, 10, 5)
        
        enviado = st.form_submit_button("Salvar Avaliação")
        
        if enviado:
            novo_dado = pd.DataFrame([[nome, data, d, i, s, c]], columns=['Nome', 'Data', 'D', 'I', 'S', 'C'])
            novo_dado.to_csv(DB_FILE, mode='a', header=False, index=False)
            st.success(f"Avaliação de {nome} salva com sucesso!")

# --- ABA 2: DASHBOARD ---
with aba_dashboard:
    st.header("Evolução do Time")
    df = carregar_dados()
    
    if not df.empty:
        df['Data'] = pd.to_datetime(df['Data'])
        df = df.sort_values('Data')

        # Gráfico de Evolução Média
        st.subheader("Média do Time ao Longo do Tempo")
        df_media = df.groupby('Data')[['D', 'I', 'S', 'C']].mean()
        st.line_chart(df_media)

        # Comparação Individual
        st.subheader("Comparação por Colaborador")
        pessoa = st.selectbox("Escolha um membro para ver detalhes", df['Nome'].unique())
        df_pessoa = df[df['Nome'] == pessoa]
        
        fig, ax = plt.subplots()
        df_pessoa.set_index('Data')[['D', 'I', 'S', 'C']].plot(kind='bar', ax=ax)
        plt.title(f"Evolução de {pessoa}")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("Nenhum dado registrado ainda.")