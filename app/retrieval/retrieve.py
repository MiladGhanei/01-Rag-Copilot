import json, faiss, numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import STORE, INDEX, EMB_MODEL

class Retriever:
    def __init__(self):
        self.embed = SentenceTransformer(EMB_MODEL)
        self.index = faiss.read_index(INDEX)
        self.meta = [json.loads(l) for l in open(STORE, encoding="utf-8")]

    def search(self, query: str, k: int = 6, top_n: int = 4):
        q = self.embed.encode([query], normalize_embeddings=True)
        D, I = self.index.search(np.asarray(q, dtype="float32"), k)
        hits = [(self.meta[i] | {"score": float(D[0][j])}) for j, i in enumerate(I[0])]
        return hits[:top_n]