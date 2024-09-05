import ollama


class Ollama3Wrapper:
    """
    Um wrapper para a interação com o modelo Ollama 3, facilitando o processamento de textos e a extração de vetores.

    Atributos:
    ----------
    model_name : str
        Nome do modelo Ollama 3 a ser utilizado.
    client : ollama.Client
        Instância do cliente Ollama para interagir com o modelo.

    Métodos:
    --------
    __init__(model_name: str)
        Inicializa o Ollama3Wrapper com o nome do modelo e cria uma instância do cliente Ollama.

    processar(texto: str) -> dict
        Processa um texto usando o modelo Ollama 3 e retorna uma estrutura contendo os vetores extraídos.
    """

    def __init__(self, model_name: str):
        """
        Inicializa o Ollama3Wrapper com o nome do modelo e cria uma instância do cliente Ollama.

        Parâmetros:
        -----------
        model_name : str
            Nome do modelo Ollama 3 a ser utilizado.
        """
        self.model_name = model_name
        self.client = ollama.Client()  # Ajuste se necessário para criar um cliente

    def processar(self, texto: str) -> dict:
        """
        Processa um texto usando o modelo Ollama 3 e retorna uma estrutura contendo os vetores extraídos.

        Parâmetros:
        -----------
        texto : str
            Texto a ser processado pelo modelo Ollama 3.

        Retorna:
        --------
        dict
            Dicionário contendo os vetores extraídos, sob a chave 'vetores'. Se a resposta não contiver 'embeddings',
            será retornado o texto como uma lista, ajustado conforme necessário.

        Lança:
        ------
        ValueError
            Se não for possível converter a string para uma lista de vetores.
        """
        response = self.client.generate(
            model=self.model_name,
            prompt=texto,
        )

        # Ajuste a forma como você extrai os embeddings dependendo da estrutura real da resposta
        if "embeddings" in response:
            vetores = response["embeddings"]
        else:
            # Se a resposta não contém 'embeddings', faça a extração apropriada
            vetores = response.get("text", [])  # Ajuste conforme necessário

        # Verificar a estrutura de vetores
        if isinstance(vetores, str):
            try:
                import ast

                vetores = ast.literal_eval(
                    vetores
                )  # Converte a string para uma lista, se necessário
            except (ValueError, SyntaxError) as e:
                raise ValueError(
                    "Não foi possível converter a string para uma lista de vetores. Erro: {}".format(
                        e
                    )
                )

        return {"vetores": vetores}
