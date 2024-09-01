from chromadb import Client

client = Client(host='chroma', port=3306)
collection = client.create_collection("privacy_policy")

def store_vectors(text, vectors):
    collection.add(texts=[text], embeddings=[vectors])

def retrieve_vectors(query):
    return collection.query(query)
