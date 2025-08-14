# ...existing code...
from .embed import embed_texts
from .store import query

def search(query_text, k=12):
    qv = embed_texts([query_text])[0]
    res = query(qv, k=k)
    hits = []
    for i in range(len(res["ids"][0])):
        hits.append({
            "id": res["ids"][0][i],
            "doc": res["documents"][0][i],
            "meta": res["metadatas"][0][i],
            "score": 1 - res["distances"][0][i],
        })
    return hits
