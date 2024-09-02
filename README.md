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
- **Sentence Transformers** 📖
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

execute:

```bash
pip install -r requirements.txt
```

## 🏃‍♂️ Uso

### 1. Prepare Seu PDF

Coloque o arquivo PDF na mesma pasta que o script principal ou forneça o caminho para ele. 📂

### 2. Execute a Aplicação

- **No Windows:**

  ```bash
  streamlit run main.py
  ```

- **No Linux/macOS:**

  ```bash
  streamlit run main.py
  ```

Isso iniciará a aplicação Streamlit em seu navegador padrão. 🌐

### 3. Interaja com a Aplicação

- **Upload do PDF:** Arraste e solte seu arquivo PDF na área designada para fazer o upload. 📤
- **Consulta:** Após o upload, digite sua consulta na caixa de texto e clique no botão de enviar. A aplicação retornará uma resposta baseada no conteúdo do PDF. 🧐


## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes. 📜

