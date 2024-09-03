# Use a imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Instala o Ollama CLI
RUN curl -fsSL https://ollama.com/download/ollama-linux-x64 -o /usr/local/bin/ollama && \
    chmod +x /usr/local/bin/ollama

# Baixa o modelo llama3
RUN ollama pull llama3

# Copia todo o conteúdo do projeto para o diretório de trabalho no container
COPY . .

# Exposição da porta usada pelo Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação Streamlit
CMD ["streamlit", "run", "app.py"]
