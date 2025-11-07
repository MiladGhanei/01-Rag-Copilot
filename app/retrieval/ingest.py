from pathlib import Path
import json, uuid
from pypdf import PdfReader
from app.core.config import DOCS_DIR, STORE

def run(docs_dir=DOCS_DIR, out_path=STORE):
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        for pdf in Path(docs_dir).glob("*.pdf"):
            r = PdfReader(str(pdf))
            for i, page in enumerate(r.pages, 1):
                txt = (page.extract_text() or "").strip()
                if txt: f.write(json.dumps({"id": str(uuid.uuid4()), "doc": pdf.name, "page": i, "text": txt})+"\n")