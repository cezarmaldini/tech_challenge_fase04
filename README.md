# 🧠 Tech Challenge | Fase 4 - Modelo Preditivo dos Níveis de Obesidade

Projeto desenvolvido como parte da Fase 4 da PÓS TECH em Data Analytics, com o objetivo de aplicar técnicas de ciência de dados e machine learning para prever níveis de obesidade, apoiando equipes médicas em diagnósticos preventivos.


## 📌 Contextualização do Problema

O desafio proposto consiste em atuar como cientista de dados de um hospital para desenvolver um sistema preditivo capaz de estimar o **nível de obesidade** de um paciente com base em características pessoais, hábitos alimentares e estilo de vida.


## 🔎 Análise Exploratória

A análise exploratória foi conduzida no **Microsoft Fabric** através do notebook [`nb_analise_exploratoria.ipynb`](./nb_analise_exploratoria.ipynb).

Principais pontos abordados:
- Distribuição das variáveis categóricas e numéricas
- Correlações entre variáveis
- Transformações aplicadas para normalização e codificação

A análise permitiu compreender os padrões entre os fatores de risco e os níveis de obesidade, além de direcionar quais variáveis utilizar para treinamento do modelo.

---

## 🤖 Treinamento do Modelo Preditivo

O treinamento do modelo foi feito também no **Microsoft Fabric**, utilizando o notebook [`nb_modelo_preditivo.ipynb`](./nb_modelo_preditivo.ipynb).

### Algoritmo Utilizado:
- **RandomForestClassifier**

### Métricas de Desempenho:
```text
Acurácia: 0.9196

              precision    recall  f1-score   support

  Obesidade Grau I       0.96      0.96      0.96        70
 Obesidade Grau II       0.98      1.00      0.99        60
Obesidade Grau III       1.00      1.00      1.00        65
 Peso Insuficiente       0.88      0.93      0.90        54
       Peso Normal       0.81      0.81      0.81        58
 Sobrepeso Nível I       0.89      0.86      0.88        58
Sobrepeso Nível II       0.89      0.86      0.88        58

   Accuracy                          0.92       423
  Macro avg        0.92      0.92      0.92       423
Weighted avg       0.92      0.92      0.92       423

```

## 🌐 Aplicação com Streamlit

A aplicação foi desenvolvida com **Streamlit**, e o código principal encontra-se em [`app.py`](./app.py).

### Funcionalidades

#### 📊 Dashboard Analítico
- Métricas gerais e distribuição dos níveis de obesidade
- Análises interativas de:
  - Gênero
  - Histórico familiar de obesidade
  - Hábito de fumar
  - Consumo de alimentos calóricos
- Comportamentos:
  - Comer entre refeições
  - Consumo de álcool
  - Meio de transporte utilizado
- Correlações:
  - Nível de obesidade por gênero
  - Histórico familiar por obesidade
  - Faixa etária e prática de atividades físicas

As visualizações utilizam **Plotly** com gráficos de barras, pizza e linhas interativas, organizadas com layout responsivo via Streamlit.

#### 🧪 Previsão com Modelo Preditivo
- Formulário para entrada de dados de pacientes
  - Gênero, idade, peso
  - Hábitos alimentares e estilo de vida
- Resultado previsto:
  - Nível de obesidade (7 possíveis categorias)
  - Mensagem orientativa com base no resultado
- Modelo treinado previamente e carregado no início da aplicação

O objetivo da aplicação é **suportar decisões médicas** com base em dados, oferecendo uma **visão analítica completa** e **previsões personalizadas** para cada paciente.

### Acesse a Solução:
🔗 [tech-challenge-fase3.onrender.com](https://tech-challenge-fase04.onrender.com)

## 🛢 Banco de Dados

- Os dados utilizados na aplicação foram **persistidos em um banco de dados PostgreSQL**, permitindo:
  - Armazenamento estruturado e seguro
  - Integração direta com o modelo preditivo para previsões em tempo real
  - Possibilidade de expansão futura da base com novos dados clínicos

---

## 🚀 Deploy

A aplicação foi **containerizada com Docker** e publicada na nuvem utilizando a plataforma **Render Cloud**, garantindo:

- Deploy automatizado e escalável
- Ambiente isolado e replicável para produção
- Facilidade de atualização contínua

---

## 🧰 Tecnologias Utilizadas

| Categoria           | Ferramenta/Ferramentas                      |
|---------------------|---------------------------------------------|
| Linguagem           | Python 3.11                                 |
| Ambiente Notebook   | Microsoft Fabric                            |
| Machine Learning    | scikit-learn, pandas, numpy                 |
| Visualização        | Plotly, Streamlit                           |
| Dashboard Interativo| Streamlit + Plotly                          |
| Banco de Dados      | PostgreSQL                                  |
| Deploy              | Docker, Render Cloud                        |
| Gerenciador de Pacotes | pip, requirements.txt                    |

## 📦 Arquivo `requirements.txt`

Abaixo estão listadas todas as dependências utilizadas no projeto, e que devem ser instaladas para o correto funcionamento da aplicação:

```
streamlit
streamlit-option-menu
pandas
plotly
python-dotenv
sqlalchemy
psycopg2-binary
scikit-learn
```

Você pode instalar todas com o comando:
```
pip install -r requirements.txt
```

## 🐳 Dockerfile

O projeto está preparado para ser executado em um container Docker. O arquivo Dockerfile contém a seguinte configuração:

```
# Imagem base oficial do Python
FROM python:3.11

# Define o diretório de trabalho no container
WORKDIR /app

# Copia os arquivos da aplicação para o container
COPY . /app

# Instala dependências
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expõe a porta usada pelo Streamlit
EXPOSE 8501

# Comando para rodar a aplicação Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## ⭐ Contribua com o Projeto

Se você gostou deste projeto e ele foi útil de alguma forma, considere deixar uma estrela ⭐ no repositório para apoiar o trabalho!


Desenvolvido por:
👨‍💻 Cézar Maldini Rocha Almeida

