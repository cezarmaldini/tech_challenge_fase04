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