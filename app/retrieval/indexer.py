import json, faiss, numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import STORE, INDEX, EMB_MODEL

def run(store=STORE, index_path=INDEX, model_name=EMB_MODEL):
    model = SentenceTransformer(model_name)
    texts = [json.loads(l)["text"] for l in open(store, encoding="utf-8")]
    embs = model.encode(texts, normalize_embeddings=True, batch_size=64, show_progress_bar=True)
    ix = faiss.IndexFlatIP(embs.shape[1]); ix.add(np.asarray(embs, dtype="float32"))
    faiss.write_index(ix, index_path)