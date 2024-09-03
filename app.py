import streamlit as st
import os
import shutil

from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate

from src.pdf_utils import extrair_texto_pdf, extract_text_to_documents
from src.ollama_utils import Ollama3Wrapper
from src.chromadb_utils import ChromaDBWrapper

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar o modelo e o armazenamento de vetores
cached_llm = Ollama(model="llama3")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

embedding = FastEmbedEmbeddings()
folder_path = "db"

# Definindo o novo template de prompt com contexto concatenado
new_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é uma IA que responde a todas as perguntas sobre um documento PDF enviado por usuários. Você só responde em português.",
        ),
        ("user", "{input}\n\nContexto:\n{context}"),
    ]
)

# Configurações
model_name = os.getenv("LANGCHAIN_MODEL", "ollama3")
chromadb_url = os.getenv("CHROMADB_URL", "chroma_db_url")

# Inicializar Ollama3 e ChromaDB
ollama = Ollama3Wrapper(model_name)
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
        """
        Processa o texto extraído do PDF e armazena os vetores gerados no banco de dados.

        O texto extraído é dividido em chunks usando `RecursiveCharacterTextSplitter`, e cada chunk é convertido em vetores usando `FastEmbedEmbeddings`. Os vetores são armazenados no banco de dados usando `Chroma` e persistidos no diretório especificado por `folder_path`.
        """
        chunks = text_splitter.split_documents(documents)
        vector_store = Chroma.from_documents(
            documents=chunks, embedding=embedding, persist_directory=folder_path
        )
        vector_store.persist()

        st.write("Texto processado e vetores armazenados com sucesso!")

    # Consulta ao banco de dados
    consulta = st.text_input("Digite sua consulta")

    if st.button("Consultar"):
        """
        Consulta o banco de dados usando a ChromaDB e retorna uma resposta gerada pelo modelo Ollama3.

        A consulta é feita no banco de dados para recuperar documentos relevantes. Os documentos recuperados são utilizados para gerar uma resposta usando o modelo Ollama3. O resultado inclui a resposta gerada e fontes relevantes, que são exibidas ao usuário.
        """
        # Recuperar os vetores relevantes para a consulta
        consulta_resultado = db.consulta(consulta)

        # Verifique se a consulta retornou documentos relevantes
        if not consulta_resultado:
            st.error("Nenhum documento relevante encontrado.")

        vector_store = Chroma(
            persist_directory=folder_path, embedding_function=embedding
        )

        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 20,
                "score_threshold": 0.9,
            },
        )

        document_chain = create_stuff_documents_chain(cached_llm, new_prompt)
        chain = create_retrieval_chain(retriever, document_chain)

        # Realizar a consulta e obter o resultado
        try:
            result = chain.invoke({"input": consulta, "context": consulta_resultado})
            sources = []
            for doc in result.get("context", []):
                sources.append(
                    {
                        "source": doc.metadata.get("source", "Desconhecido"),
                        "page_content": doc.page_content,
                    }
                )

            response_answer = {
                "answer": result.get("answer", "Nenhuma resposta encontrada."),
                "sources": sources,
            }
            st.write(
                f"""
            
            ## Resposta

            {response_answer["answer"]}

            """
            )
        except Exception as e:
            st.error(f"Erro ao processar a consulta: {e}")

    # Remover o arquivo temporário
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
