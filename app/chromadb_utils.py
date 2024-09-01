from chromadb import Client

class ChromaDBWrapper:
    """
    Um wrapper para a interação com o ChromaDB, facilitando a criação, armazenamento e consulta em uma coleção de vetores.

    Attributes:
        client (Client): Instância do cliente ChromaDB para interagir com o banco de dados.
        db_url (str): URL do banco de dados ChromaDB.
        collection_name (str): Nome da coleção de vetores a ser usada.
        collection (Collection): Instância da coleção de vetores no ChromaDB.

    Methods:
        __init__(db_url):
            Inicializa a instância do ChromaDBWrapper, criando ou recuperando a coleção de vetores.

        armazena(vetores):
            Armazena uma lista de vetores na coleção ChromaDB.

        consulta(consulta):
            Consulta a coleção ChromaDB e retorna os resultados baseados em uma consulta fornecida.
    """

    def __init__(self, db_url):
        """
        Inicializa a instância do ChromaDBWrapper, criando ou recuperando a coleção de vetores.

        Args:
            db_url (str): URL do banco de dados ChromaDB para a conexão.
        """
        self.client = Client()  # Inicialize o cliente conforme a documentação
        self.db_url = db_url
        
        # Nome da coleção
        self.collection_name = 'data-doc'
        
        # Verificar se a coleção já existe
        collections = self.client.list_collections()
        print("Exibindo coleções:")
        print(collections)

        if self.collection_name in collections:
            self.collection = self.client.get_collection(self.collection_name)
            print(f"Coleção '{self.collection_name}' recuperada com sucesso.")
        else:
            try:
                # Tente criar a coleção
                self.collection = self.client.create_collection(name=self.collection_name)
                print(f"Coleção '{self.collection_name}' criada com sucesso.")
            except Exception as e:
                # Captura qualquer exceção genérica e trata como erro na criação
                print(f"Erro ao criar a coleção: {e}")
                # Recupera a coleção existente se a criação falhar
                self.collection = self.client.get_collection(self.collection_name)
                print(f"Coleção '{self.collection_name}' já existia. Recuperada com sucesso.")

    def armazena(self, vetores):
        """
        Armazena uma lista de vetores na coleção ChromaDB.

        Args:
            vetores (list or str): Lista de vetores a serem armazenados. Se for uma string, deve ser convertida para uma lista de vetores.

        Raises:
            ValueError: Se a conversão de string para lista falhar ou se os vetores não estiverem no formato esperado.
        """
        if isinstance(vetores, str):
            # Se vetores for uma string, tente converter a string para uma lista de vetores
            try:
                import ast
                vetores = ast.literal_eval(vetores)  # Converte a string para uma lista
            except (ValueError, SyntaxError) as e:
                raise ValueError("Não foi possível converter a string para uma lista de vetores. Erro: {}".format(e))
        
        if not isinstance(vetores, list):
            raise ValueError("Esperava uma lista de vetores, mas recebeu: {}".format(type(vetores)))
        
        for vetor in vetores:
            if not isinstance(vetor, list):
                raise ValueError("Esperava um vetor como lista, mas recebeu: {}".format(type(vetor)))
            self.collection.add(vetor)  # Adiciona vetores à coleção

    def consulta(self, consulta):
        """
        Consulta a coleção ChromaDB e retorna os resultados baseados em uma consulta fornecida.

        Args:
            consulta (str): O texto da consulta para buscar na coleção.

        Returns:
            dict: Resultados da consulta na coleção, baseados na implementação da API ChromaDB.

        Notes:
            A consulta é realizada com o texto fornecido e o formato dos resultados depende da implementação do método `query`.
        """
      
        print(self.collection.count())
        resultados = self.collection.query(query_texts=[consulta])  # Ajuste conforme a API real
        return resultados
