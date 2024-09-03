Aqui está o README atualizado com as instruções detalhadas sobre Docker e Ollama, bem como o link para o vídeo de teste:

---

# 📚 Aplicação de Recuperação Aumentada de Conhecimento (RAG) com Ollama 3

Bem-vindo ao projeto de Recuperação Aumentada de Conhecimento (RAG) usando o modelo Ollama 3! 🎉 Este projeto oferece uma solução robusta para extrair e consultar informações de arquivos PDF. Vamos começar! 🚀

## 🌟 Funcionalidades

- **Extração de Texto:** Extraia texto de arquivos PDF de maneira eficiente. 📄
- **Armazenamento e Recuperação:** Armazene e recupere informações extraídas de PDFs. 🗃️
- **Consultas Inteligentes:** Realize consultas e obtenha respostas precisas baseadas no conteúdo do PDF. 🤖

## 📋 Requisitos

Certifique-se de ter os seguintes pacotes instalados:

- **Python 3.10 ou superior** 🐍
- **Ollama 3** 📦
- **ChromaDB** 📊
- **PyMuPDF** 📚

## 📥 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/thaleson/case_starsoft
cd seu_repositorio
```

### 2. Crie e Ative um Ambiente Virtual

- **No Windows:**

  ```bash
  python -m venv env
  .\env\Scripts\activate
  ```

- **No Linux/macOS:**

  ```bash
  python3 -m venv env
  source env/bin/activate
  ```

### 3. Instale as Dependências

Execute:

```bash
pip install -r requirements.txt
```

## 🐳 Uso com Docker

Se preferir usar Docker para rodar a aplicação, siga os passos abaixo:

### 1. Crie o Dockerfile

Certifique-se de que o `Dockerfile` no diretório raiz do projeto está configurado corretamente. Exemplo de `Dockerfile`:

```dockerfile
# Use a imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do projeto para o diretório de trabalho no container
COPY . .

# Exposição da porta usada pelo Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação Streamlit
CMD ["streamlit", "run", "main.py"]
```

### 2. Crie o arquivo `docker-compose.yml`

Configure o arquivo `docker-compose.yml` para incluir o Ollama e o ChromaDB. Exemplo:

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./db:/app/db
    environment:
      - STREAMLIT_SERVER_ENABLE_CORS=false
      - STREAMLIT_SERVER_HEADLESS=true
    depends_on:
      - chromadb
      - ollama

  chromadb:
    image: nouchka/sqlite3
    ports:
      - "8000:8000"
    volumes:
      - ./db:/data
    environment:
      - SQLITE_DATABASE=/data/chroma.sqlite3

  ollama:
    image: your-ollama-image
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_MODEL=llama3
    volumes:
      - ./models:/models
```

### 3. Inicie os Contêineres

Execute:

```bash
docker-compose up
```

Certifique-se de que o contêiner do Ollama está configurado para rodar o modelo `llama3` e está acessível na porta 11434.

## 📹 Vídeo de Teste

Veja o vídeo testando a aplicação: [Vídeo de Teste](https://www.youtube.com/watch?v=Wiu-epVUAQo&t=53s)

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 📜

