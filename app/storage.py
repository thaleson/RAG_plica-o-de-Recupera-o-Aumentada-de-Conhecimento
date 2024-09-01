# app/storage.py
def store_data(processed_text: str) -> None:
    """
    Armazena o texto processado. 

    :param processed_text: Texto processado a ser armazenado.
    """
    try:
        with open("data/processed_text.txt", "w") as file:
            file.write(processed_text)
    except Exception as e:
        raise RuntimeError(f"Erro ao armazenar os dados: {e}")
