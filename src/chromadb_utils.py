from chromadb import Client, Collection

class ChromaDBWrapper:
    def __init__(self, db_url: str):
        """
        Inicializa o ChromaDBWrapper com a URL do banco de dados e configura a coleção.

        Parâmetros:
        -----------
        db_url : str
            URL do banco de dados ChromaDB.
        """
        self.client = Client()  # Verifique se a criação do cliente está correta
        self.db_url = db_url

        # Nome da coleção
        self.collection_name = "data-doc"

        # Verificar se a coleção já existe
        try:
            collections = self.client.list_collections()
            print("Exibindo coleções:")
            print(collections)

            if self.collection_name in collections:
                self.collection = self.client.get_collection(self.collection_name)
                print(f"Coleção '{self.collection_name}' recuperada com sucesso.")
            else:
                # Tente criar a coleção
                self.collection = self.client.create_collection(
                    name=self.collection_name
                )
                print(f"Coleção '{self.collection_name}' criada com sucesso.")
        except AttributeError as e:
            print(f"Erro ao interagir com o cliente ChromaDB: {e}")
            raise

    def armazena(self, vetores):
        if isinstance(vetores, str):
            try:
                import ast
                vetores = ast.literal_eval(vetores)  # Converte a string para uma lista
            except (ValueError, SyntaxError) as e:
                raise ValueError(f"Não foi possível converter a string para uma lista de vetores. Erro: {e}")

        if not isinstance(vetores, list):
            raise ValueError(f"Esperava uma lista de vetores, mas recebeu: {type(vetores)}")

        for vetor in vetores:
            if not isinstance(vetor, list):
                raise ValueError(f"Esperava um vetor como lista, mas recebeu: {type(vetor)}")
            self.collection.add(vetor)

    def consulta(self, consulta: str) -> dict:
        print(self.collection.count())
        resultados = self.collection.query(
            query_texts=[consulta]
        )
        return resultados
