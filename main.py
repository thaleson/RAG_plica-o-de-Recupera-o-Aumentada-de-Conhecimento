import streamlit as st
from app.pdf_reader import read_pdf
from app.text_processor import process_text
from models.huggingface_api import HuggingFaceAPI
from time import sleep

def main():
    """
    Função principal que inicializa a aplicação Streamlit.
    """
    st.title("Aplicação de Recuperação Aumentada de Conhecimento (RAG)")

    uploaded_file = st.file_uploader("Escolha um PDF", type="pdf")
    
    if uploaded_file:
        file_path = "data/uploaded.pdf"
        
        # Salve o arquivo PDF localmente
        with open(file_path, "wb") as file:
            file.write(uploaded_file.read())
        
        # Leia o PDF
        text = read_pdf(file_path)
        
        # Exiba o texto extraído do PDF
        st.subheader("Texto Extraído do PDF")
        st.text_area("Texto Extraído", text, height=300)
        
        # Exibir indicador de carregamento
        with st.spinner('Processando o texto...'):
            sleep(1)  # Simula o tempo de carregamento (remova ou ajuste conforme necessário)
            try:
                processed_text = process_text(text)

                # Criar instância da API Hugging Face
                hf_api = HuggingFaceAPI()
                
                # Processar o texto com modelos NLP
                summary = hf_api.hierarchical_summary(processed_text)
                classification = hf_api.classify_text(processed_text)
                entities = hf_api.extract_entities(processed_text)
                
                # Exiba os resultados
                st.subheader("Resumo do Texto")
                st.write(summary)
                
                st.subheader("Classificação do Texto")
                if isinstance(classification, list) and len(classification) > 0:
                    label = classification[0].get('label', 'Desconhecido')
                    score = classification[0].get('score', 0.0)
                    st.write(f"Classificação: {label} com score de {score:.2f}")
                else:
                    st.write("Classificação não disponível. Verifique o modelo e a entrada.")
                
                st.subheader("Entidades Extraídas")
                if entities:
                    for entity in entities:
                        st.write(f"Entidade: {entity.get('word', 'Desconhecida')}, Tipo: {entity.get('entity', 'Desconhecido')}, Score: {entity.get('score', 0.0):.2f}")
                else:
                    st.write("Nenhuma entidade extraída.")
                
            except Exception as e:
                st.error(f"Ocorreu um erro durante o processamento: {e}")
        
        st.success("Texto processado, analisado e armazenado com sucesso!")

if __name__ == "__main__":
    main()
