# src/pdf_utils.py

from PyPDF2 import PdfReader
from langchain_community.document_loaders import PDFPlumberLoader

def extrair_texto_pdf(pdf_file):
    """
    Extrai o texto de um arquivo PDF.

    Args:
        pdf_file (file-like object): O arquivo PDF do qual o texto será extraído. Deve ser um objeto compatível com o formato esperado pela PyPDF2.

    Returns:
        str: O texto extraído do arquivo PDF.
    """
    texto = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        texto += page.extract_text()
    return texto

def extract_text_to_documents(pdf_file):
    """
    Converte um arquivo PDF em uma lista de documentos usando o PDFPlumberLoader.

    Args:
        pdf_file (file-like object): O arquivo PDF a ser carregado. Deve ter um atributo 'name' que representa o nome do arquivo.

    Returns:
        list: Uma lista de documentos extraídos do arquivo PDF. O formato exato dos documentos depende da implementação do PDFPlumberLoader.
    """
    loader = PDFPlumberLoader("data/" + pdf_file.name)
    docs = loader.load_and_split()

    return docs
