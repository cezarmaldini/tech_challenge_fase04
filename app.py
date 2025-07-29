import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from modelo import treinar_modelo

from queries import (
    metricas_gerais, distribuicao_obesidade, obter_genero, obter_historico_familiar,
    obter_fumantes, obter_favc, metricas_caec, metricas_calc, metricas_mtrans,
    distribuicao_genero_por_obesidade, media_faf_por_nivel_obesidade, casos_por_obesidade_e_hist_fam,
    obesidade_faixa_etaria
)

@st.cache_resource
def carregar_modelo():
    return treinar_modelo()

pipeline = carregar_modelo()

# ===========================================================
# Configuração inicial da aplicação
st.set_page_config(
    page_title='Analytics',
    page_icon='📊',
    layout='wide'
)

# ===========================================================
# Navegação da Aplicação
with st.sidebar:
    option = option_menu(
        menu_title="Navegação",
        options=["Dashboard", "Modelo Preditivo"],
        icons=["bar-chart", "graph-up-arrow"],
        menu_icon="card-list",
        default_index=0
    )
# ===========================================================
# Página Dashboard
if option == 'Dashboard':
    st.title('📊 Dashboard')
    st.divider()

    # =======================================================
    # Métricas Gerais
    st.subheader('Métricas Gerais')
    metricas = metricas_gerais().iloc[0]

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric('Total de amostras', int(metricas['total_amostras']))
    col2.metric('Obesidade (%)', f"{metricas['pct_obesidade']:.2f}%")
    col3.metric('Sobrepeso (%)', f"{metricas['pct_sobrepeso']:.2f}%")
    col4.metric('Peso normal (%)', f"{metricas['pct_peso_normal']:.2f}%")
    col5.metric('Peso insuficiente (%)', f"{metricas['pct_peso_insuficiente']:.2f}%")

    # Gráfico de barras - Distribuição dos Níveis de Obesidade
    df_dist = distribuicao_obesidade()

    fig = px.bar(
        df_dist,
        x='Nivel_Obesidade',
        y='count',
        title='Distribuição dos Níveis de Obesidade',
        text='count',
        color='Nivel_Obesidade',
        labels={'Nivel_Obesidade': 'Nível de Obesidade', 'count': 'Quantidade'}
    )

    fig.update_layout(
        xaxis_title='Nível de Obesidade',
        yaxis_title='Quantidade',
        xaxis_tickangle=-45
    )

    st.plotly_chart(fig)

    st.divider()
    # ====================================================
    # Análises Categóricas
    st.subheader('Análises Categóricas')

    df_gender = obter_genero()
    df_gender.columns = ['Gênero', 'Quantidade']

    df_hist = obter_historico_familiar()
    df_hist.columns = ['Histórico Familiar', 'Quantidade']

    df_smoke = obter_fumantes()
    df_smoke.columns = ['Fuma?', 'Quantidade']

    df_favc = obter_favc()
    df_favc.columns = ['FAVC', 'Quantidade']

    fig = make_subplots(rows=1, cols=4, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                        subplot_titles=['Gênero', 'Histórico Familiar Excesso de Peso', 'Fuma?', 'Consome alimentos calóricos frequentemente?'])

    fig.add_trace(go.Pie(labels=df_gender['Gênero'],
                        values=df_gender['Quantidade'],
                        name='Gênero', hole=0.4,
                        textinfo='percent+label'),
                row=1, col=1)

    fig.add_trace(go.Pie(labels=df_hist['Histórico Familiar'],
                        values=df_hist['Quantidade'],
                        name='Histórico Familiar', hole=0.4,
                        textinfo='percent+label'),
                row=1, col=2)

    fig.add_trace(go.Pie(labels=df_smoke['Fuma?'],
                        values=df_smoke['Quantidade'],
                        name='Fuma?', hole=0.4, rotation=45,
                        textinfo='percent+label'),
                row=1, col=3)
        
    fig.add_trace(go.Pie(labels=df_favc['FAVC'],
                            values=df_favc['Quantidade'],
                            name='FAVC', hole=0.4, rotation=45,
                            textinfo='percent+label'),
                row=1, col=4)

    fig.update_layout(height=400, showlegend=False)

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ====================================================
    # Análises Comportamentais
    st.subheader('Análises Comportamentais')

    df_caec = metricas_caec()
    df_calc = metricas_calc()
    df_mtrans = metricas_mtrans()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.plotly_chart(
            px.bar(df_caec,
                   x='categoria',
                   y='quantidade',
                   title='Comer entre as refeições',
                   color_discrete_sequence=['#636EFA'],
                   labels={'categoria': 'Categoria', 'quantidade': 'Quantidade'},
                   text_auto='.f'
                ), use_container_width=True)

    with col2:
        st.plotly_chart(
            px.bar(df_calc,
                   x='categoria',
                   y='quantidade',
                   title='Frequência do consumo de álcool',
                   color_discrete_sequence=['#EF553B'],
                   labels={'categoria': 'Categoria', 'quantidade': 'Quantidade'},
                   text_auto='.f'
                ), use_container_width=True)

    with col3:
        st.plotly_chart(
            px.bar(df_mtrans,
                   x='categoria',
                   y='quantidade',
                   title='Meio de Transporte utilizado',
                   color_discrete_sequence=['#00CC96'],
                   labels={'categoria': 'Categoria', 'quantidade': 'Quantidade'},
                   text_auto='.f'
                ), use_container_width=True)

    st.divider()
    # ====================================================
    # Análises por Níveis de Obesidade
    st.subheader('Análises por Níveis de Obesidade')

    col1, col2 = st.columns(2)

    with col1:
        df_genero_obesidade = distribuicao_genero_por_obesidade()
        df_pivot = df_genero_obesidade.pivot(index='Nivel_Obesidade', columns='Genero', values='quantidade').fillna(0)

        fig = px.bar(
            df_pivot,
            orientation='h',
            barmode='stack',
            title='Distribuição de Gênero por Nível de Obesidade',
            labels={'value': 'Quantidade', 'Nivel_Obesidade': 'Nível de Obesidade'},
            text_auto='.f',
            color_discrete_sequence=px.colors.qualitative.Plotly
        )

        st.plotly_chart(fig, use_container_width=True)

        df = casos_por_obesidade_e_hist_fam()

        ordem = [
            'Peso Insuficiente',
            'Peso Normal',
            'Sobrepeso Nível I',
            'Sobrepeso Nível II',
            'Obesidade Grau I',
            'Obesidade Grau II',
            'Obesidade Grau III'
        ]

        df["Nivel_Obesidade"] = pd.Categorical(df["Nivel_Obesidade"], categories=ordem, ordered=True)
        df = df.sort_values("Nivel_Obesidade")

        fig = px.line(
            df,
            x="Nivel_Obesidade",
            y="total_casos",
            color="Historico_Familiar",
            markers=True,
            title="Total de Casos por Nível de Obesidade e Histórico Familiar",
            labels={'total_casos': 'Quantidade', 'Nivel_Obesidade': 'Nível de Obesidade', 'Historico_Familiar': 'Histórico Familiar'}
        )
        st.plotly_chart(fig)

    with col2:
        df = media_faf_por_nivel_obesidade()

        fig = px.bar(
            df,
            x="media_faf",
            y="Nivel_Obesidade",
            orientation="h",
            color="Nivel_Obesidade",
            title="Prática de exercício físico por Nível de Obesidade",
            labels={'media_faf': 'Média Prática de Exercícios', 'Nivel_Obesidade': 'Nível de Obesidade'},
            text_auto='.2f'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig)

        df = obesidade_faixa_etaria()

        ordem = [
            'Menor de 18', '18-30', '31-40',
            '41-50', '50+'
        ]
        df["Faixa_Etaria"] = pd.Categorical(df["Faixa_Etaria"], categories=ordem, ordered=True)
        df = df.sort_values("Faixa_Etaria")

        fig = px.bar(
            df,
            x="Faixa_Etaria",
            y="total_casos",
            color="Nivel_Obesidade",
            barmode="group",
            title="Casos por Nível de Obesidade e Faixa Etária",
            labels={'Faixa_Etaria': 'Faixa Etária', 'Nivel_Obesidade': 'Nível de Obesidade', 'total_casos': 'Quantidade'}
        )

        st.plotly_chart(fig, use_container_width=True)                                            

# ===========================================================
# Modelo Preditivo
elif option == 'Modelo Preditivo':
    st.title("🧪 Modelo Preditivo")

    st.divider()

    st.markdown("""
        O modelo preditivo apresentado tem como objetivo oferecer suporte à tomada de decisão, prevendo o **nível de obesidade** de um paciente com base em **características de perfil, hábitos alimentares e estilo de vida.**

        A proposta é permitir que profissionais e gestores da área de saúde, bem-estar ou alimentação possam utilizar a ferramenta para antecipar riscos e promover ações preventivas, alinhando tecnologia e inteligência de dados à geração de valor nos negócios.
        """)
    
    st.divider()

    st.subheader('Formulário')
    with st.expander('Responda o formulário abaixo para realizar a previsão com base nos dados inseridos.'):
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
            calc = st.selectbox("Com que frequência consome álcool?", ["Às vezes", "Frequentemente", "Sempre", "Não"])
            mtrans = st.selectbox("Qual meio de transporte utiliza?", ["Transporte Público", "Andando", "Automóvel", "Motocicleta", "Bicicleta"])

    if st.button("🧪 Realizar Previsão"):
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
        nivel = resultado[0]

        st.session_state["nivel_obesidade"] = nivel

        mensagem = {
            "Peso Insuficiente": "Você está abaixo do peso ideal. É importante buscar orientação médica e nutricional para avaliar sua saúde geral.",
            "Peso Normal": "Parabéns! Seu peso está dentro da faixa considerada saudável. Continue mantendo bons hábitos!",
            "Sobrepeso Nível I": "Você está no primeiro nível de sobrepeso. Reavaliar hábitos alimentares e atividades físicas pode ajudar a voltar ao peso ideal.",
            "Sobrepeso Nível II": "Você está no segundo nível de sobrepeso. Mudanças nos hábitos e acompanhamento profissional são recomendados.",
            "Obesidade Grau I": "Você está com obesidade tipo I. É essencial adotar mudanças no estilo de vida e buscar acompanhamento profissional.",
            "Obesidade Grau II": "Você está com obesidade tipo II. Isso pode trazer riscos à saúde. Acompanhamento médico e nutricional são fortemente recomendados.",
            "Obesidade Grau III": "Você está com obesidade tipo III (grave). Essa condição demanda atenção médica imediata."
        }

        st.success(f"Nível de obesidade previsto: **{nivel}**")
        st.info(mensagem.get(nivel, "Informação não disponível para este nível."))