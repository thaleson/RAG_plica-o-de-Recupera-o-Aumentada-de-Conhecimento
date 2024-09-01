

import ollama

class Ollama3Wrapper:
    """
    Um wrapper para a classe Ollama3 que facilita a interação com o modelo para geração de vetores de texto.

    Attributes:
        model_name (str): Nome do modelo a ser utilizado pela instância do Ollama3Wrapper.
        client (ollama.Client): Instância do cliente Ollama para gerar respostas do modelo.

    Methods:
        __init__(model_name):
            Inicializa a instância do Ollama3Wrapper com o nome do modelo e cria um cliente Ollama.

        processar(texto):
            Gera vetores a partir do texto usando o modelo Ollama e retorna os vetores extraídos.
    """

    def __init__(self, model_name):
        """
        Inicializa a instância do Ollama3Wrapper com o nome do modelo e cria um cliente Ollama.

        Args:
            model_name (str): O nome do modelo a ser utilizado pela instância do Ollama3Wrapper.
        """
        self.model_name = model_name
        self.client = ollama.Client()  # Ajuste se necessário para criar um cliente

    def processar(self, texto):
        """
        Gera vetores a partir do texto usando o modelo Ollama e retorna os vetores extraídos.

        Args:
            texto (str): O texto para o qual os vetores devem ser gerados pelo modelo Ollama.

        Returns:
            dict: Um dicionário contendo os vetores gerados pelo modelo. A chave é 'vetores', e o valor é uma lista de vetores extraídos do modelo.
        
        Raises:
            ValueError: Se a conversão da string para uma lista de vetores falhar.
        """
        response = self.client.generate(
            model=self.model_name,
            prompt=texto,
        )
        
        # Ajuste a forma como você extrai os embeddings dependendo da estrutura real da resposta
        if 'embeddings' in response:
            vetores = response['embeddings']
        else:
            # Se a resposta não contém 'embeddings', faça a extração apropriada
            vetores = response.get('text', [])  # Ajuste conforme necessário
        
        # Verificar a estrutura de vetores
        if isinstance(vetores, str):
            try:
                import ast
                vetores = ast.literal_eval(vetores)  # Converte a string para uma lista, se necessário
            except (ValueError, SyntaxError) as e:
                raise ValueError("Não foi possível converter a string para uma lista de vetores. Erro: {}".format(e))
        
        return {'vetores': vetores}
