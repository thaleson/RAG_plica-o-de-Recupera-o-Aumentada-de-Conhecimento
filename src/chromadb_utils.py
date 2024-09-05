from chromadb import Client

class ChromaDBWrapper:
    """
    Um wrapper para a interação com o ChromaDB, facilitando o gerenciamento de coleções e armazenamento de vetores.

    Atributos:
    ----------
    client : Client
        Instância do cliente ChromaDB para interação com o banco de dados.
    db_url : str
        URL do banco de dados ChromaDB.
    collection_name : str
        Nome da coleção usada para armazenar e consultar vetores.
    collection : Collection
        Instância da coleção usada para armazenar e consultar vetores.

    Métodos:
    --------
    __init__(db_url: str)
        Inicializa o ChromaDBWrapper com a URL do banco de dados e configura a coleção.

    armazena(vetores: list)
        Armazena uma lista de vetores na coleção do ChromaDB.

    consulta(consulta: str) -> dict
        Consulta a coleção do ChromaDB com um texto de consulta e retorna os resultados.
    """

    def __init__(self, db_url: str):
        """
        Inicializa o ChromaDBWrapper com a URL do banco de dados e configura a coleção.

        Parâmetros:
        -----------
        db_url : str
            URL do banco de dados ChromaDB.
        """
        self.client = Client()  # Inicialize o cliente conforme a documentação
        self.db_url = db_url

        # Nome da coleção
        self.collection_name = "data-doc"

        # Conectar ao ChromaDB
        self.client.set_url(self.db_url)

        # Verificar se a coleção já existe
        try:
            collections = self.client.list_collections()
            print("Exibindo coleções:")
            print(collections)

            if self.collection_name in collections:
                self.collection = self.client.get_collection(self.collection_name)
                print(f"Coleção '{self.collection_name}' recuperada com sucesso.")
            else:
                self.collection = self.client.create_collection(
                    name=self.collection_name
                )
                print(f"Coleção '{self.collection_name}' criada com sucesso.")
        except Exception as e:
            print(f"Erro ao acessar ou criar a coleção: {e}")
            raise

    def armazena(self, vetores):
        """
        Armazena uma lista de vetores na coleção do ChromaDB.

        Parâmetros:
        -----------
        vetores : list
            Lista de vetores a serem armazenados. Cada vetor deve ser uma lista.

        Lança:
        ------
        ValueError
            Se `vetores` não for uma lista ou se algum vetor dentro da lista não for uma lista.
        """
        if isinstance(vetores, str):
            try:
                import ast
                vetores = ast.literal_eval(vetores)
            except (ValueError, SyntaxError) as e:
                raise ValueError(
                    "Não foi possível converter a string para uma lista de vetores. Erro: {}".format(e)
                )

        if not isinstance(vetores, list):
            raise ValueError(
                "Esperava uma lista de vetores, mas recebeu: {}".format(type(vetores))
            )

        for vetor in vetores:
            if not isinstance(vetor, list):
                raise ValueError(
                    "Esperava um vetor como lista, mas recebeu: {}".format(type(vetor))
                )
            self.collection.add(vetor)  # Adiciona vetores à coleção

    def consulta(self, consulta: str) -> dict:
        """
        Consulta a coleção do ChromaDB com um texto de consulta e retorna os resultados.

        Parâmetros:
        -----------
        consulta : str
            Texto de consulta para buscar na coleção do ChromaDB.

        Retorna:
        --------
        dict
            Resultados da consulta, formatados conforme a API real do ChromaDB.
        """
        try:
            print(self.collection.count())
            resultados = self.collection.query(
                query_texts=[consulta]
            )  # Ajuste conforme a API real
            return resultados
        except Exception as e:
            print(f"Erro ao consultar a coleção: {e}")
            raise
