import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from modelo import treinar_modelo
from agent import buscar_informacoes_complementares

@st.cache_resource
def carregar_modelo():
    return treinar_modelo()

pipeline = carregar_modelo()

# Confiuração inicial da aplicação
st.set_page_config(
    page_title='Analytics',
    page_icon='📊',
    layout='wide'
)

# Navegação da Aplicação
with st.sidebar:
    option = option_menu(
        menu_title="Navegação",
        options=["Home", "Dashboard", "Modelo Preditivo"],
        icons=["house", "bar-chart", "graph-up-arrow"],
        menu_icon="card-list",
        default_index=0
    )

if option == 'Home':
    st.title('Comece por aqui')

elif option == 'Modelo Preditivo':
    # Interface com Streamlit
    st.title("Modelo Preditivo")

    col1, col2 = st.columns(2)

    with col1:
        genero = st.selectbox("Gênero", ["Masculino", "Feminino"])
        peso = st.number_input("Peso (kg)", min_value=30.0, max_value=500.0, value=70.0)
        historico_familiar = st.selectbox("Histórico familiar de obesidade", ["Sim", "Não"])
        favc = st.selectbox("Consome alimentos calóricos com frequência?", ["Sim", "Não"])
        caec = st.selectbox("Come entre as refeições?", ["Às vezes", "Frequentemente", "Sempre", "Não"])
    with col2:
        scc = st.selectbox("Monitora calorias?", ["Sim", "Não"])
        faf = st.slider("Frequência de atividade física", 0.0, 3.0, 1.0)
        calc = st.selectbox("Frequência de álcool", ["Às vezes", "Frequentemente", "Sempre", "Não"])
        mtrans = st.selectbox("Meio de transporte", ["Transporte Público", "Andando", "Automóvel", "Motocicleta", "Bicicleta"])

    # Predição
    if st.button("Prever nível de obesidade"):
        entrada = pd.DataFrame([{
            'Genero': genero,
            'Peso': peso,
            'Historico_Familiar': historico_familiar,
            'FAVC': favc,
            'CAEC': caec,
            'SCC': scc,
            'FAF': faf,
            'CALC': calc,
            'MTRANS': mtrans
        }])
        
        resultado = pipeline.predict(entrada)
        mensagem = {
            "Peso Insuficiente": "Você está abaixo do peso ideal. É importante buscar orientação médica e nutricional para avaliar sua saúde geral.",
            "Peso Normal": "Parabéns! Seu peso está dentro da faixa considerada saudável. Continue mantendo bons hábitos!",
            "Sobrepeso Nível I": "Você está no primeiro nível de sobrepeso. Reavaliar hábitos alimentares e atividades físicas pode ajudar a voltar ao peso ideal.",
            "Sobrepeso Nível II": "Você está no segundo nível de sobrepeso. Mudanças nos hábitos e acompanhamento profissional são recomendados.",
            "Obesidade Grau I": "Você está com obesidade tipo I. É essencial adotar mudanças no estilo de vida e buscar acompanhamento profissional.",
            "Obesidade Grau II": "Você está com obesidade tipo II. Isso pode trazer riscos à saúde. Acompanhamento médico e nutricional são fortemente recomendados.",
            "Obesidade Grau III": "Você está com obesidade tipo III (grave). Essa condição demanda atenção médica imediata."
        }

        nivel = resultado[0]
        st.success(f"Nível de obesidade previsto: **{nivel}**")
        st.info(mensagem.get(nivel, "Informação não disponível para este nível."))