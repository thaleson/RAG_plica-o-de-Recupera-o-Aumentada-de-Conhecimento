from chromadb import Client

class ChromaDBWrapper:
    def __init__(self, db_url: str):
        """
        Inicializa o ChromaDBWrapper com a URL do banco de dados e configura a coleção.
        """
        self.client = Client(url=db_url)  # Certifique-se de passar a URL corretamente
        self.collection_name = "data-doc"

        # Verificar se a coleção já existe
        collections = self.client.list_collections()
        if self.collection_name in collections:
            self.collection = self.client.get_collection(self.collection_name)
        else:
            self.collection = self.client.create_collection(self.collection_name)

    def armazena(self, vetores):
        if not isinstance(vetores, list):
            raise ValueError("Esperava uma lista de vetores.")
        for vetor in vetores:
            if not isinstance(vetor, list):
                raise ValueError("Esperava um vetor como lista.")
            self.collection.add(vetor)  # Adiciona vetores à coleção

    def consulta(self, consulta: str) -> dict:
        resultados = self.collection.query(query_texts=[consulta])
        return resultados
