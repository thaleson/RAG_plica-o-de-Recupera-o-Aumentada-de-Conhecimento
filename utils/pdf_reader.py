"""
Utilitário para leitura de PDFs.

Contém funções auxiliares para ler e extrair texto de arquivos PDF.
"""

import pdfplumber

def ler_pdf(caminho_pdf: str) -> str:
    """
    Lê e extrai o texto de um arquivo PDF.

    Args:
        caminho_pdf (str): Caminho do arquivo PDF.

    Returns:
        str: Texto extraído do PDF.
    """
    with pdfplumber.open(caminho_pdf) as pdf:
        texto = "".join([pagina.extract_text() for pagina in pdf.pages])
    return texto
