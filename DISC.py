import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Teste DISC Profissional", layout="wide")
DB_FILE = "dados_disc_v2.csv"

# Dicionário de adjetivos baseados na metodologia DISC
# Cada linha contém uma opção para D, I, S e C respectivamente
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
    fig.add_trace(go.Scatterpolar(r=valores, theta=categorias, fill='toself', name=nome))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10])), showlegend=False)
    return fig

st.title("📊 Avaliação de Perfil DISC")

aba_form, aba_dashboard = st.tabs(["📝 Realizar Teste", "📈 Análise do Time"])

with aba_form:
    st.header("Escolha a palavra que melhor descreve você em cada grupo:")
    
    with st.form("teste_disc"):
        nome_user = st.selectbox("Selecione seu nome", ["Ana", "Bruno", "Caio", "Duda", "Enzo", "Fernanda", "Guto", "Helô", "Igor", "Julia"])
        
        # Dicionário para armazenar os pontos
        pontos = {"D": 0, "I": 0, "S": 0, "C": 0}
        
        # Gerar as perguntas baseadas no dicionário QUESTOES
        for i, q in enumerate(QUESTOES):
            st.write(f"**Grupo {i+1}**")
            # Misturamos as opções para não ficarem sempre na mesma ordem (D, I, S, C)
            opcoes = [q["D"], q["I"], q["S"], q["C"]]
            escolha = st.radio(f"Qual dessas palavras mais se aplica a você?", opcoes, key=f"q{i}", horizontal=True)
            
            # Atribuir ponto à categoria correta
            if escolha == q["D"]: pontos["D"] += 1
            elif escolha == q["I"]: pontos["I"] += 1
            elif escolha == q["S"]: pontos["S"] += 1
            elif escolha == q["C"]: pontos["C"] += 1
        
        enviado = st.form_submit_button("Finalizar e Salvar Perfil")
        
        if enviado:
            perfil_dom = max(pontos, key=pontos.get)
            data_atual = datetime.now().strftime('%d/%m/%Y')
            
            novo_dado = pd.DataFrame([[nome_user, data_atual, pontos['D'], pontos['I'], pontos['S'], pontos['C'], perfil_dom]], 
                                     columns=['Nome', 'Data', 'D', 'I', 'S', 'C', 'Perfil'])
            
            novo_dado.to_csv(DB_FILE, mode='a', header=not os.path.exists(DB_FILE), index=False)
            
            st.success(f"Obrigado, {nome_user}! Seu perfil predominante é: {perfil_dom}")
            st.plotly_chart(gerar_radar([pontos['D'], pontos['I'], pontos['S'], pontos['C']], nome_user))

with aba_dashboard:
    df = carregar_dados()
    if not df.empty:
        st.header("Dashboard de Evolução do Time")
        
        # Filtro por colaborador
        colab = st.selectbox("Ver histórico de:", df['Nome'].unique())
        df_colab = df[df['Nome'] == colab]
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.write(f"### Último Perfil: {df_colab.iloc[-1]['Perfil']}")
            st.plotly_chart(gerar_radar([df_colab.iloc[-1]['D'], df_colab.iloc[-1]['I'], df_colab.iloc[-1]['S'], df_colab.iloc[-1]['C']], colab))
        
        with col2:
            st.write("### Evolução ao longo do tempo")
            df_colab_display = df_colab.set_index('Data')[['D', 'I', 'S', 'C']]
            st.line_chart(df_colab_display)
            
        st.write("---")
        # Botão de Backup para você não perder os dados online
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar Planilha de Dados Atualizada", csv, "dados_disc.csv", "text/csv")
    else:
        st.info("Nenhuma resposta registrada ainda.")