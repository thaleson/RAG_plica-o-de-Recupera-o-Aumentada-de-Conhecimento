import requests

class Llama3APIWrapper:
    """
    Um wrapper para a interação com o modelo Llama 3, facilitando o processamento de textos e a geração de respostas.

    Atributos:
    ----------
    base_url : str
        URL base da API do Llama 3.
    api_key : str
        Chave da API para autenticação.

    Métodos:
    --------
    __init__(base_url: str, api_key: str)
        Inicializa o Llama3APIWrapper com a URL base e a chave da API.

    __call__(prompt: str) -> str
        Envia um prompt para o modelo Llama 3 e retorna a resposta gerada.
    """

    def __init__(self, base_url: str, api_key: str):
        """
        Inicializa o Llama3APIWrapper com a URL base e a chave da API.

        Parâmetros:
        -----------
        base_url : str
            URL base da API do Llama 3.
        api_key : str
            Chave da API para autenticação.
        """
        self.base_url = base_url
        self.api_key = api_key

    def __call__(self, prompt: str) -> str:
        """
        Envia um prompt para o modelo Llama 3 e retorna a resposta gerada.

        Parâmetros:
        -----------
        prompt : str
            Texto a ser enviado para o modelo Llama 3.

        Retorna:
        --------
        str
            Resposta gerada pelo modelo Llama 3.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": "meta/llama3-70b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.6,
            "top_p": 1,
            "max_tokens": 1024,
            "stream": False,  # Alterado para False para facilitar a depuração
        }
        response = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result:
                return result["choices"][0]["message"]["content"]
            else:
                return "Resposta não encontrada."
        else:
            return f"Erro ao acessar a API: {response.status_code}, {response.text}"
