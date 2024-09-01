from transformers import pipeline
from typing import Dict, Any

class HuggingFaceAPI:
    def __init__(self):
        """
        Inicializa a API do Hugging Face com pipelines pré-treinados.
        """
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.classifier = pipeline("text-classification", model="neuralmind/bert-base-portuguese-cased")
        self.ner = pipeline("ner", model="neuralmind/bert-base-portuguese-cased")

    def summarize_text(self, text: str) -> str:
        """
        Resumir o texto usando o Hugging Face.
        
        Args:
            text (str): Texto a ser resumido.
        
        Returns:
            str: Resumo do texto.
        """
        summary = self.summarizer(text, max_length=150, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Classificar o texto usando o Hugging Face.
        
        Args:
            text (str): Texto a ser classificado.
        
        Returns:
            Dict[str, Any]: Classificação do texto.
        """
        classification = self.classifier(text)
        return classification

    def extract_entities(self, text: str) -> Dict[str, Any]:
        """
        Extrair entidades do texto usando o Hugging Face.
        
        Args:
            text (str): Texto do qual extrair entidades.
        
        Returns:
            Dict[str, Any]: Entidades extraídas.
        """
        entities = self.ner(text)
        return entities

    def hierarchical_summary(self, text: str) -> str:
        """
        Resumir o texto de forma hierárquica.
        
        Args:
            text (str): Texto a ser resumido.
        
        Returns:
            str: Resumo hierárquico do texto.
        """
        # Implementar o resumo hierárquico aqui
        return "Resumo hierárquico do texto."
