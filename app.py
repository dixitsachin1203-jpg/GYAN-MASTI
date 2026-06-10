import streamlit as st
from pypdf import PdfReader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="GyanMasti.ai",
    page_icon="🤖",
    layout="wide"
)

# ----------------------------------
# STYLING
# ----------------------------------

st.markdown("""
<style>

.stApp{
background: linear-gradient(
135deg,
#020617,
#0f172a,
#111827
);
color:white;
}

.main-title{
font-size:55px;
font-weight:800;
text-align:center;
background:linear-gradient(90deg,#00F5FF,#00FF9D);
-webkit-background-clip:text;
-webkit-text-fill-color:transparent;
}

.subtitle{
text-align:center;
color:#94a3b8;
font-size:18px;
}

.chat-user{
background:#1e293b;
padding:15px;
border-radius:15px;
margin:10px;
}

.chat-ai{
background:#0f766e;
padding:15px;
border-radius:15px;
margin:10px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------
# HEADER
# ----------------------------------

st.markdown(
"""
<div class="main-title">
🤖 GyanMasti.ai
</div>

<div class="subtitle">
Learn Smarter • Revise Faster • Score Better
</div>
""",
unsafe_allow_html=True
)

# ----------------------------------
# SESSION
# ----------------------------------

if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

if "messages" not in st.session_state:
    st.session_state.messages = []

# ----------------------------------
# SIDEBAR
# ----------------------------------

with st.sidebar:

    st.header("📚 Upload Notes")

    pdfs = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    process = st.button("🚀 Build Knowledge Base")

# ----------------------------------
# PDF PROCESSING
# ----------------------------------

if process and pdfs:

    with st.spinner("Reading PDFs..."):

        text = ""

        for pdf in pdfs:

            reader = PdfReader(pdf)

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_text(text)

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.from_texts(
            chunks,
            embeddings
        )

        llm = OllamaLLM(
            model="llama3"
        )

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(
                search_kwargs={"k": 4}
            )
        )

        st.session_state.qa_chain = qa_chain

    st.success("Knowledge Base Ready!")

# ----------------------------------
# CHAT HISTORY
# ----------------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ----------------------------------
# CHAT INPUT
# ----------------------------------

question = st.chat_input(
    "Ask anything from your uploaded notes..."
)

if question:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        if st.session_state.qa_chain is None:

            answer = """
Please upload PDFs and build the knowledge base first.
"""

        else:

            with st.spinner("🧠 Thinking..."):

                answer = st.session_state.qa_chain.run(
                    question
                )

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )
