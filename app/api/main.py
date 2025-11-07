from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from app.retrieval.retrieve import Retriever
from fastapi import FastAPI, UploadFile, File
from pathlib import Path
import shutil
from app.retrieval import ingest as ingest_mod, indexer as indexer_mod

app = FastAPI(title="RAG Copilot (MVP)")
ret = Retriever()
gen = pipeline("text2text-generation", model="google/flan-t5-base")  # CPU-friendly

def build_prompt(question, ctx):
    blocks = []
    for i, c in enumerate(ctx, 1):
        blocks.append(f"[{i}] {c['text']}\n(META: {c['doc']} p{c['page']})")
    context = "\n\n".join(blocks)
    return (
        "Answer using ONLY the numbered context. If not answerable, say: "
        "'I don't know based on the context.' Keep it concise (2–5 sentences).\n\n"
        f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
    )

class AskReq(BaseModel):
    question: str

@app.post("/ask")
def ask(req: AskReq):
    ctx = ret.search(req.question)
    prompt = build_prompt(req.question, ctx)
    ans = gen(prompt, max_new_tokens=180)[0]["generated_text"].strip()
    sources = [{"doc": c["doc"], "page": c["page"]} for c in ctx]
    return {"answer": ans, "sources": sources}

@app.post("/ingest")
async def ingest_pdf(file: UploadFile = File(...)):
    dst = Path("data/docs"); dst.mkdir(parents=True, exist_ok=True)
    with open(dst / file.filename, "wb") as f:
        shutil.copyfileobj(file.file, f)
    ingest_mod.run()         # rebuild store.jsonl
    indexer_mod.run()        # rebuild FAISS
    global ret; ret = Retriever()  # reload retriever
    return {"ok": True, "file": file.filename}