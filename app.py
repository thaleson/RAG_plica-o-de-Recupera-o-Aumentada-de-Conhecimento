import streamlit as st
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

from app.pdf_utils import extrair_texto_pdf, extract_text_to_documents
from app.ollama_utils import Ollama3Wrapper
from app.chromadb_utils import ChromaDBWrapper

# Inicializar o modelo e o armazenamento de vetores
cached_llm = Ollama(model="llama3")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

embedding = FastEmbedEmbeddings()
folder_path = "db"

raw_prompt = PromptTemplate.from_template(
    """ 
    <s>[INST] Você é um assistente técnico bom em pesquisar documentos. Se você não tiver uma resposta com base nas informações fornecidas, diga-o [/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
"""
)

# Configurações
model_name = os.getenv('LANGCHAIN_MODEL', 'ollama3')
chromadb_url = os.getenv('CHROMADB_URL', 'chroma_db_url')

# Inicializar Ollama3 e ChromaDB
ollama = Ollama3Wrapper(model_name)
db = ChromaDBWrapper(chromadb_url)

# Configuração da interface Streamlit
st.title("Aplicação de Recuperação Aumentada de Conhecimento (RAG)")

# Upload do arquivo PDF
uploaded_file = st.file_uploader("Escolha um arquivo PDF", type="pdf")

if uploaded_file is not None:
    # Extrair texto do PDF
    texto = extrair_texto_pdf(uploaded_file)
    documents = extract_text_to_documents(uploaded_file)
    
    st.write("Texto extraído do PDF:")
    st.write(texto)

    # Processar o texto do PDF
    if st.button("Processar Texto"):
        """
        Processa o texto extraído do PDF e armazena os vetores gerados no banco de dados.
        
        O texto é dividido em chunks, convertido em vetores e armazenado usando o ChromaDB.
        """
        print(f"docs len={len(documents)}")

        chunks = text_splitter.split_documents(documents)
        print(f"chunks len={len(chunks)}")

        vector_store = Chroma.from_documents(
            documents=chunks, embedding=embedding, persist_directory=folder_path
        )

        vector_store.persist()

        print('texto')
        print(texto)
        print("# processando no llama")
        resultado = ollama.processar(texto)
        vetores = resultado.get('vetores', [])
        
        if isinstance(vetores, str):
     
            st.error("Os vetores retornados são uma string. Esperado uma lista de vetores.")
        else:
            
            db.armazena(vetores)
            st.write("Texto processado e vetores armazenados com sucesso!")

    # Consulta ao banco de dados
    consulta = st.text_input("Digite sua consulta")
    
    if st.button("Consultar"):
        """
        Consulta o banco de dados usando a ChromaDB e retorna uma resposta gerada pelo modelo Ollama3.
        
        A consulta é realizada para recuperar documentos relevantes e gerar uma resposta baseada no contexto.
        """
        resultado_consulta = db.consulta(consulta)
        vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

        print("Creating chain")
        retriever = vector_store.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={
                "k": 20,
                "score_threshold": 0.1,
            },
        )
        document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
        chain = create_retrieval_chain(retriever, document_chain)

        result = chain.invoke({"input": consulta})
        sources = []
        for doc in result["context"]:
            sources.append(
                {"source": doc.metadata["source"], "page_content": doc.page_content}
            )

        response_answer = {"answer": result["answer"], "sources": sources}
        st.write(response_answer)

        
