from langchain import LangChain

class LangChainWrapper:
    """
    Um wrapper para a classe LangChain que facilita o uso do modelo para processamento de texto.

    Attributes:
        langchain (LangChain): Instância da classe LangChain configurada com o modelo especificado.

    Methods:
        __init__(model_name):
            Inicializa a instância do LangChainWrapper com o modelo especificado.

        processar(texto):
            Processa o texto usando o modelo LangChain e retorna o resultado.
    """

    def __init__(self, model_name):
        """
        Inicializa a instância do LangChainWrapper com o modelo especificado.

        Args:
            model_name (str): O nome do modelo a ser utilizado pela instância do LangChain.
        """
        self.langchain = LangChain(model=model_name)

    def processar(self, texto):
        """
        Processa o texto usando o modelo LangChain e retorna o resultado.

        Args:
            texto (str): O texto a ser processado pelo modelo LangChain.

        Returns:
            Resultado do processamento do texto pelo modelo LangChain. O tipo de retorno depende da implementação do método 'processar' do modelo LangChain.
        """
        return self.langchain.processar(texto)
