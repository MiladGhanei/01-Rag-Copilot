.PHONY: ingest index api ui

ingest:
	python -c "from app.retrieval.ingest import run; run()"

index:
	python -c "from app.retrieval.indexer import run; run()"

api:
	uvicorn app.api.main:app --reload

ui:
	streamlit run app/ui/app.py
