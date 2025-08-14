# ...existing code...
from sentence_transformers import SentenceTransformer

_model = None

def load_model(name):
    global _model
    _model = SentenceTransformer(name)

def embed_texts(texts):
    return _model.encode(texts, batch_size=64, show_progress_bar=False, normalize_embeddings=True)
