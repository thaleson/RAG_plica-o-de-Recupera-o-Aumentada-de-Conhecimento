from PyPDF2 import PdfReader
from langchain_community.document_loaders import PDFPlumberLoader


def extrair_texto_pdf(pdf_file):
    """
    Extrai todo o texto de um arquivo PDF e retorna como uma única string.

    Parâmetros:
    -----------
    pdf_file : str
        O caminho para o arquivo PDF do qual o texto será extraído.

    Retorna:
    --------
    str
        O texto extraído de todas as páginas do PDF concatenado em uma única string.

    Exceções:
    ----------
    O método `PdfReader` pode lançar exceções se o arquivo PDF estiver corrompido ou inacessível.
    """
    texto = ""
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        texto += page.extract_text()
    return texto


def extract_text_to_documents(file_path):
    """
    Extrai texto de um arquivo PDF e retorna uma lista de documentos no formato esperado pelo `PDFPlumberLoader`.

    Parâmetros:
    -----------
    file_path : str
        O caminho para o arquivo PDF do qual o texto será extraído e convertido em documentos.

    Retorna:
    --------
    list
        Uma lista de documentos extraídos do PDF, cada um representando um segmento do texto.

    Exceções:
    ----------
    O método `PDFPlumberLoader.load` pode lançar exceções se o arquivo PDF estiver corrompido, inacessível,
    ou se o formato do arquivo não for compatível com o loader.
    """
    loader = PDFPlumberLoader(file_path)
    documents = loader.load()
    return documents
