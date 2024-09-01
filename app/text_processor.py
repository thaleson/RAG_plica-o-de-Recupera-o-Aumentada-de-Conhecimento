# app/text_processor.py
from typing import List
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import torch

# Carregando o modelo e o tokenizer do DistilBERT
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased')

def process_text(text: str) -> str:
    """
    Processa o texto usando o modelo DistilBERT.

    :param text: Texto a ser processado.
    :return: Resultados do processamento.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Supondo que o modelo esteja configurado para uma tarefa de classificação
    logits = outputs.logits
    predictions = torch.argmax(logits, dim=-1)
    
    return f"Predições: {predictions.item()}"
