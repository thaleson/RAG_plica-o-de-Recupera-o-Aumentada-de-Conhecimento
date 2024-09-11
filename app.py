import streamlit as st
import os
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from src.ollama_utils import Llama3APIWrapper
from src.pdf_utils import extrair_texto_pdf, extract_text_to_documents
from src.chromadb_utils import ChromaDBWrapper
import requests
import json

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar o modelo e o armazenamento de vetores com a chave da API
llama3_api_key = os.getenv("API_KEY")
llama3_base_url = "https://integrate.api.nvidia.com/v1"


# Inicializar o modelo Llama3
llama3_model = Llama3APIWrapper(base_url=llama3_base_url, api_key=llama3_api_key)

# Inicializar outros componentes
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)
embedding = FastEmbedEmbeddings()
folder_path = "db"

# Definindo o novo template de prompt com contexto concatenado
new_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é uma IA que responde a todas as perguntas sobre um documento PDF enviado por usuários. Você só responde em português.",
        ),
        ("user", "{input}\n\nContexto:\n{context}"),
    ]
)

# Função para gerar o prompt completo a partir do template
def generate_prompt(input_text, context):
    return new_prompt_template.format(input=input_text, context=context)

# Configurações
chromadb_url = os.getenv("CHROMADB_URL", "chroma_db_url")
db = ChromaDBWrapper(chromadb_url)

# Configuração da interface Streamlit
st.title("Aplicação de Recuperação Aumentada de Conhecimento (RAG)")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

if uploaded_file is not None:
    # Salvar o arquivo PDF carregado em um diretório temporário
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.read())
        temp_file_path = temp_file.name

    # Extrair texto do PDF
    texto = extrair_texto_pdf(temp_file_path)
    documents = extract_text_to_documents(temp_file_path)

    st.write("Texto extraído do PDF:")
    st.write(texto)

    # Processar o texto do PDF
    if st.button("Processar Texto"):
        chunks = text_splitter.split_documents(documents)
        vector_store = Chroma.from_documents(
            documents=chunks, embedding=embedding, persist_directory=folder_path
        )
        vector_store.persist()
        st.write("Texto processado e vetores armazenados com sucesso!")

    # Consulta ao banco de dados
    consulta = st.text_input("Digite sua consulta")

    if st.button("Consultar") and consulta:
        vector_store = Chroma(
            persist_directory=folder_path, embedding_function=embedding
        )
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 20,
                "score_threshold": 0.5,
            },
        )

        # Obter contexto dos documentos mais relevantes
        context = ""
        results = retriever.get_relevant_documents(consulta)
        if results:
            context = " ".join(doc.page_content for doc in results)

        # Gere o prompt completo com o contexto extraído
        prompt = generate_prompt(consulta, context)
        
        # Use o wrapper como um "Runnable" aqui
        try:
            result = llama3_model(prompt)
            st.write(f"""
                     ## Resposta
                      \n\n{result}""")
        except Exception as e:
            st.error(f"Erro ao processar a consulta: {e}")

    # Remover o arquivo temporário
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)