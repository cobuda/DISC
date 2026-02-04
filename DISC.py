import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Portal DISC - Equipe", layout="wide")
DB_FILE = "dados_disc_v2.csv"

# LISTA ATUALIZADA DE COLABORADORES
COLABORADORES = [
    "Daniel", "Danilo", "Francielle", "Hency", "Lucas", "Marco", 
    "Mateus", "Natan", "Paulo", "Rick", "Silvana", "Thiago"
]

# Dicionário de adjetivos DISC
QUESTOES = [
    {"D": "Determinado", "I": "Persuasivo", "S": "Gentil", "C": "Habilidoso"},
    {"D": "Competitivo", "I": "Entusiasta", "S": "Paciente", "C": "Lógico"},
    {"D": "Ousado", "I": "Sociável", "S": "Estável", "C": "Preciso"},
    {"D": "Direto", "I": "Comunicativo", "S": "Moderado", "C": "Perfeccionista"},
    {"D": "Decidido", "I": "Convincente", "S": "Conciliador", "C": "Analítico"},
    {"D": "Autoconfiante", "I": "Otimista", "S": "Acolhedor", "C": "Disciplinado"},
    {"D": "Independente", "I": "Animado", "S": "Previsível", "C": "Cauteloso"},
    {"D": "Energético", "I": "Influente", "S": "Amigável", "C": "Sistemático"},
    {"D": "Focado", "I": "Expressivo", "S": "Colaborativo", "C": "Detalhista"},
    {"D": "Líder", "I": "Espontâneo", "S": "Atencioso", "C": "Organizado"}
]

def carregar_dados():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=['Nome', 'Data', 'D', 'I', 'S', 'C', 'Perfil'])

def gerar_radar(valores, nome):
    categorias = ['Dominância', 'Influência', 'Estabilidade', 'Conformidade']
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=valores + [valores[0]],
        theta=categorias + [categorias[0]],
        fill='toself',
        line=dict(color='#636EFA'),
        name=nome
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=False,
        title=f"Perfil de {nome}"
    )
    return fig

st.title("📊 Avaliação de Perfil DISC - Time")

aba_form, aba_dashboard = st.tabs(["📝 Realizar Teste", "📈 Painel do Gestor"])

with aba_form:
    st.header("Formulário Comportamental")
    with st.form("teste_disc"):
        nome_user = st.selectbox("Selecione seu nome:", sorted(COLABORADORES))
        st.divider()
        
        pontos = {"D": 0, "I": 0, "S": 0, "C": 0}
        
        for i, q in enumerate(QUESTOES):
            st.write(f"**Questão {i+1}:** Qual palavra melhor descreve você?")
            opcoes = [q["D"], q["I"], q["S"], q["C"]]
            escolha = st.radio("", opcoes, key=f"q{i}", horizontal=True, label_visibility="collapsed")
            
            if escolha == q["D"]: pontos["D"] += 1
            elif escolha == q["I"]: pontos["I"] += 1
            elif escolha == q["S"]: pontos["S"] += 1
            elif escolha == q["C"]: pontos["C"] += 1
        
        enviado = st.form_submit_button("Salvar Minha Avaliação")
        
        if enviado:
            perfil_dom = max(pontos, key=pontos.get)
            data_atual = datetime.now().strftime('%Y-%m-%d')
            novo_dado = pd.DataFrame([[nome_user, data_atual, pontos['D'], pontos['I'], pontos['S'], pontos['C'], perfil_dom]], 
                                     columns=['Nome', 'Data', 'D', 'I', 'S', 'C', 'Perfil'])
            novo_dado.to_csv(DB_FILE, mode='a', header=not os.path.exists(DB_FILE), index=False)
            st.success(f"Excelente, {nome_user}! Seus dados foram salvos.")
            st.plotly_chart(gerar_radar([pontos['D'], pontos['I'], pontos['S'], pontos['C']], nome_user))

with aba_dashboard:
    df = carregar_dados()
    if not df.empty:
        # Visão Geral do Time
        st.header("Análise do Time")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Média D", round(df['D'].mean(), 1))
        col2.metric("Média I", round(df['I'].mean(), 1))
        col3.metric("Média S", round(df['S'].mean(), 1))
        col4.metric("Média C", round(df['C'].mean(), 1))
        
        st.divider()
        colab = st.selectbox("Filtrar por Colaborador:", sorted(df['Nome'].unique()))
        df_colab = df[df['Nome'] == colab].sort_values('Data')
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.subheader("Perfil Atual")
            ultimo = df_colab.iloc[-1]
            st.plotly_chart(gerar_radar([ultimo['D'], ultimo['I'], ultimo['S'], ultimo['C']], colab))
        with c2:
            st.subheader("Evolução Temporal")
            st.line_chart(df_colab.set_index('Data')[['D', 'I', 'S', 'C']])
            
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Planilha Geral", csv, "dados_equipe_disc.csv", "text/csv")
    else:
        st.info("Aguardando as primeiras respostas do time...")