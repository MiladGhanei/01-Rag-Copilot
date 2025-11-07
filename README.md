RAG Copilot — Evidence-Grounded Q&A (MVP)

A minimal, portfolio-ready RAG app that answers questions over your PDFs with retrieval + citations and a lightweight API + UI. Built to demonstrate practical GenAI skills from the Generative AI with LLMs (DeepLearning.AI + AWS) course.

⸻

✨ What’s included (tonight’s MVP)
	•	PDF → Chunks → Index: pypdf ingestion → JSONL → FAISS vector index.
	•	/ask API: retrieves top-k chunks and generates a concise answer.
	•	Simple UI (Streamlit): ask questions; see answer + sources.
	•	Upload endpoint: ingest new PDFs from the UI and rebuild the index.
	•	Makefile + .gitignore: one-liners and a clean repo.

⸻

🧱 Minimal architecture

PDFs ──► Ingest (per page JSONL) ──► Embeddings ──► FAISS Index
   UI/API ─► Retrieve top-k chunks ─► LLM prompt ─► Answer + Sources


⸻

🧰 Tech stack
	•	Python 3.11, FastAPI, Uvicorn, Streamlit
	•	sentence-transformers (embeddings), FAISS-CPU (search)
	•	transformers (LLM; flan-t5-base for CPU-friendly MVP)
	•	pypdf, pydantic, requests, Make

⸻

🚀 Quickstart

Prereqs
	•	Python 3.11 (recommended), macOS/Homebrew
	•	(Optional) GitHub repo already created

Setup

python3.11 -m venv .venv && source .venv/bin/activate
pip install --upgrade pip
pip install fastapi "uvicorn[standard]" streamlit pypdf sentence-transformers faiss-cpu transformers peft datasets bitsandbytes pydantic requests
mkdir -p data/docs

Add docs & build index

# put a few PDFs into data/docs/
make ingest
make index

Run

# terminal A
make api
# terminal B
make ui

Use
	•	Open Streamlit link; ask a question.
	•	(Optional) Use sidebar to upload a PDF → re-ingest → re-index.
	•	API test:

curl -X POST localhost:8000/ask -H "Content-Type: application/json" \
  -d '{"question":"Summarize page 1."}'


⸻

📁 Repo layout

app/
  api/         # FastAPI routes (/ask, /ingest)
  ui/          # Streamlit client
  core/        # config
  retrieval/   # ingest (PDF->JSONL), indexer (FAISS), retriever
  generation/  # (placeholder for advanced prompts/models)
  guardrails/  # (placeholder)
  eval/        # (placeholder for RAG eval)
data/          # docs/, store.jsonl, index.faiss
models/        # (future LoRA adapters)
scripts/       # (future CLI)
report/        # daily logs (_template.md, YYYY-MM-DD.md)


⸻

📝 Daily reports
	•	Template: report/_template.md
	•	Example: report/2025-11-03.md (≈45 min session: env, ingest, index, API/UI skeleton)

⸻

🧪 What’s next (planned)
	•	Better retrieval: hybrid BM25 + embeddings, cross-encoder reranking.
	•	RAG eval: RAGAS metrics; small gold Q/A set.
	•	PEFT/LoRA: tune response style & citation behavior.
	•	Docker + CI: reproducible runs, lint/tests, GitHub Actions.
	•	Security & UX: input validation, nicer UI, streaming tokens.

⸻

📚 Course → Project (key learnings applied)
	•	Prompting discipline (context-only answers, refusal when unsure).
	•	RAG pipeline: data, retrieval, prompt, generation.
	•	Lifecycle thinking: ingest → index → serve → (evaluate) → iterate.

⸻

⚖️ License

MIT (proposed). Add your name/year.

⸻

🧩 Troubleshooting
	•	Makefile “missing separator” → commands must start with a real TAB.
	•	Empty answers? Ensure data/docs/ has PDFs; rerun make ingest && make index.
	•	Slow first run? Models download on first use (Hugging Face cache).

Polished README (full eval, LoRA, Docker) will be added after the next milestones.