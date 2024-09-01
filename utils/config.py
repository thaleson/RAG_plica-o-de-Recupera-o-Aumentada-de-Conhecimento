"""
Configurações da aplicação.

Define variáveis de ambiente e constantes usadas na aplicação.
"""

import os

CHROMADB_HOST = os.getenv("CHROMADB_HOST", "localhost")
CHROMADB_PORT = os.getenv("CHROMADB_PORT", "8001")
