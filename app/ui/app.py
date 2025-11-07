import streamlit as st, requests, json

BACKEND = "http://localhost:8000"

st.title("RAG Copilot — MVP")

# Sidebar: ingest PDFs
st.sidebar.header("Ingest PDFs")
up = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])
if st.sidebar.button("Ingest") and up:
    r = requests.post(f"{BACKEND}/ingest",
                      files={"file": (up.name, up.getvalue(), "application/pdf")},
                      timeout=120)
    if r.ok:
        st.sidebar.success(f"Indexed: {r.json().get('file')}")
    else:
        st.sidebar.error(f"Error: {r.status_code} {r.text}")

# Main: ask
q = st.text_input("Ask a question about your PDFs")
if st.button("Ask") and q.strip():
    with st.spinner("Thinking..."):
        r = requests.post(f"{BACKEND}/ask", json={"question": q}, timeout=120)
    if r.ok:
        data = r.json()
        st.markdown("### Answer")
        st.write(data.get("answer", "(no answer)"))
        st.markdown("### Sources")
        for s in data.get("sources", []):
            st.write(f"- {s['doc']} p{s['page']}")
    else:
        st.error(f"Error: {r.status_code} {r.text}")