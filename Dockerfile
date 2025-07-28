# Imagem base
FROM python:3.10

# Diretório da aplicação
WORKDIR /app

# Copiar arquivos
COPY . /app

# Instalar dependências
RUN pip install --no-cache-dir pandas scikit-learn streamlit

# Expor a porta padrão do Streamlit
EXPOSE 8501

# Comando para iniciar o app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]