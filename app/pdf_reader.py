# app/pdf_reader.py
from PyPDF2 import PdfReader
from typing import List

def read_pdf(file_path: str) -> str:
    """
    Lê o conteúdo de um arquivo PDF e retorna o texto extraído.

    :param file_path: Caminho para o arquivo PDF.
    :return: Texto extraído do PDF.
    """
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        raise RuntimeError(f"Erro ao ler o PDF: {e}")
