import pandas as pd
from config.db import get_engine

def metricas_gerais():
    query = """
        SELECT
            COUNT(*) AS total_amostras,
            100.0 * SUM(CASE WHEN "Nivel_Obesidade" IN ('Obesidade Grau I', 'Obesidade Grau II', 'Obesidade Grau III') THEN 1 ELSE 0 END) / COUNT(*) AS pct_obesidade,
            100.0 * SUM(CASE WHEN "Nivel_Obesidade" IN ('Sobrepeso Nível I', 'Sobrepeso Nível II') THEN 1 ELSE 0 END) / COUNT(*) AS pct_sobrepeso,
            100.0 * SUM(CASE WHEN "Nivel_Obesidade" = 'Peso Normal' THEN 1 ELSE 0 END) / COUNT(*) AS pct_peso_normal,
            100.0 * SUM(CASE WHEN "Nivel_Obesidade" = 'Peso Insuficiente' THEN 1 ELSE 0 END) / COUNT(*) AS pct_peso_insuficiente
        FROM obesity
    """

    engine = get_engine()
    return pd.read_sql(query, con=engine)

# Função para buscar dados de distribuição dos níveis de obesidade
def distribuicao_obesidade():
    query = """
        SELECT "Nivel_Obesidade", COUNT(*) AS Count
        FROM obesity
        GROUP BY "Nivel_Obesidade"
        ORDER BY Count DESC
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)


def obter_genero():
    query = """
        SELECT "Genero", COUNT(*) AS quantidade
        FROM obesity
        GROUP BY "Genero"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def obter_historico_familiar():
    query = """
        SELECT "Historico_Familiar", COUNT(*) AS quantidade
        FROM obesity
        GROUP BY "Historico_Familiar"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def obter_fumantes():
    query = """
        SELECT "SMOKE", COUNT(*) AS quantidade
        FROM obesity
        GROUP BY "SMOKE"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def obter_favc():
    query = """
        SELECT "FAVC", COUNT(*) AS quantidade
        FROM obesity
        GROUP BY "FAVC"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def metricas_caec():
    query = """
        SELECT 
            "CAEC" AS categoria, COUNT(*) AS quantidade 
        FROM obesity 
        GROUP BY "CAEC"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def metricas_calc():
    query = """
        SELECT 
            "CALC" AS categoria, COUNT(*) AS quantidade 
        FROM obesity 
        GROUP BY "CALC"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def metricas_mtrans():
    query = """
        SELECT 
            "MTRANS" AS categoria, COUNT(*) AS quantidade 
        FROM obesity 
        GROUP BY "MTRANS"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def distribuicao_genero_por_obesidade():
    query = """
        SELECT
            "Nivel_Obesidade",
            "Genero",
            COUNT(*) AS quantidade
        FROM obesity
        GROUP BY "Nivel_Obesidade", "Genero"
        ORDER BY "Nivel_Obesidade", "Genero"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def media_faf_por_nivel_obesidade():
    query = """
        SELECT
            "Nivel_Obesidade",
            AVG("FAF"::FLOAT) AS media_faf
        FROM obesity
        WHERE "FAF" IS NOT NULL
        GROUP BY "Nivel_Obesidade"
        ORDER BY media_faf DESC
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def casos_por_obesidade_e_hist_fam():
    query = """
        SELECT
            "Nivel_Obesidade",
            "Historico_Familiar",
            COUNT(*) AS total_casos
        FROM obesity
        WHERE "Nivel_Obesidade" IS NOT NULL AND "Historico_Familiar" IS NOT NULL
        GROUP BY "Nivel_Obesidade", "Historico_Familiar"
        ORDER BY "Nivel_Obesidade"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)

def obesidade_faixa_etaria():
    query = """
        SELECT 
            "Nivel_Obesidade",
            CASE 
                WHEN "Idade" < 18 THEN 'Menor de 18'
                WHEN "Idade" BETWEEN 18 AND 29 THEN '18-30'
                WHEN "Idade" BETWEEN 30 AND 39 THEN '31-40'
                WHEN "Idade" BETWEEN 40 AND 49 THEN '41-50'
                ELSE '50+'
            END AS "Faixa_Etaria",
            COUNT(*) AS total_casos
        FROM obesity
        GROUP BY "Nivel_Obesidade", "Faixa_Etaria"
    """
    engine = get_engine()
    return pd.read_sql(query, con=engine)