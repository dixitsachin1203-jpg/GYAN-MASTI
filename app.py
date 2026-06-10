import streamlit as st
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

st.set_page_config(
    page_title="GyanMasti.ai",
    page_icon="📚",
    layout="wide"
)

st.title("📚 GyanMasti.ai")
st.subheader("Ask Questions From Your PDF Notes (Offline Version)")

model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_text(pdf_file):
    text = ""

    reader = PdfReader(pdf_file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    return text

def chunk_text(text, chunk_size=500):
    chunks = []

    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])

    return chunks

if "chunks" not in st.session_state:
    st.session_state.chunks = []

if "index" not in st.session_state:
    st.session_state.index = None

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file:

    if st.button("Process PDF"):

        with st.spinner("Reading PDF..."):

            text = extract_text(uploaded_file)

            chunks = chunk_text(text)

            embeddings = model.encode(chunks)

            dimension = embeddings.shape[1]

            index = faiss.IndexFlatL2(dimension)

            index.add(np.array(embeddings))

            st.session_state.chunks = chunks
            st.session_state.index = index

        st.success("PDF Processed Successfully!")

question = st.text_input(
    "Ask your question"
)

if question and st.session_state.index is not None:

    q_embedding = model.encode([question])

    distances, indices = st.session_state.index.search(
        np.array(q_embedding),
        k=3
    )

    st.markdown("## Answer")

    for idx in indices[0]:
        st.write(st.session_state.chunks[idx])

st.markdown("---")
st.caption("GyanMasti.ai • Offline PDF Search Assistant")
