import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline

load_dotenv()

def treinar_modelo():
    # Conexão com PostgreSQL
    url_db = os.getenv('URL_DB')

    engine = create_engine(url_db)
    
    # Leitura da tabela
    df = pd.read_sql_query("""
        SELECT "Genero", "Peso", "Historico_Familiar", "FAVC", "CAEC",
        "SCC", "FAF", "CALC", "MTRANS", "Nivel_Obesidade"
        FROM obesity
    """, con=engine)

    # Separar variáveis
    X = df.drop('Nivel_Obesidade', axis=1).copy()
    y = df['Nivel_Obesidade']

    # Garante que colunas categóricas são string
    cat_cols = ['Genero', 'Historico_Familiar', 'FAVC', 'CAEC', 'SCC', 'CALC', 'MTRANS']
    X[cat_cols] = X[cat_cols].astype(str)

    preprocessor = ColumnTransformer([
        ('cat', OneHotEncoder(drop='first'), cat_cols)
    ], remainder='passthrough')

    pipeline = Pipeline(steps=[
        ('preprocessamento', preprocessor),
        ('modelo', RandomForestClassifier(random_state=42))
    ])

    pipeline.fit(X, y)
    return pipeline