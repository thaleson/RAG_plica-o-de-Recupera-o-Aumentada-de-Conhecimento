from langchain import LangChain


class LangChainWrapper:
    """
    Um wrapper para a classe LangChain que facilita a interação com o modelo LangChain.

    Atributos:
    ----------
    langchain : LangChain
        Instância da classe LangChain configurada com o modelo especificado.

    Métodos:
    --------
    __init__(model_name: str)
        Inicializa o LangChainWrapper com o nome do modelo fornecido.

    processar(texto: str) -> str
        Processa o texto usando o modelo LangChain e retorna o resultado.
    """

    def __init__(self, model_name: str):
        """
        Inicializa o LangChainWrapper com o nome do modelo fornecido.

        Parâmetros:
        -----------
        model_name : str
            Nome do modelo a ser utilizado pelo LangChain.
        """
        self.langchain = LangChain(model=model_name)

    def processar(self, texto: str) -> str:
        """
        Processa o texto usando o modelo LangChain e retorna o resultado.

        Parâmetros:
        -----------
        texto : str
            O texto a ser processado pelo modelo LangChain.

        Retorna:
        --------
        str
            O resultado do processamento do texto pelo modelo LangChain.
        """
        return self.langchain.processar(texto)
