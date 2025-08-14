# ...existing code...
import chromadb
client = chromadb.PersistentClient(path="./chroma_store")
col = client.get_or_create_collection("jarvis", metadata={"hnsw:space": "cosine"})

def upsert(ids, embeddings, metadatas, documents):
    col.upsert(ids=ids, embeddings=embeddings, metadatas=metadatas, documents=documents)

def query(embedding, k=12):
    return col.query(query_embeddings=[embedding], n_results=k,
                     include=["documents", "metadatas", "distances", "ids"])

def reset_collection():
    col.delete()
