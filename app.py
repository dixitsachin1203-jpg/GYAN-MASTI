import os
import streamlit as st
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate

from pypdf import PdfReader

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="GyanMasti.ai",
    page_icon="📚",
    layout="wide"
)

load_dotenv()

# ======================================
# CUSTOM CSS
# ======================================

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:48px;
    font-weight:bold;
    color:#00C9A7;
}

.sub-title{
    text-align:center;
    font-size:18px;
    color:gray;
    margin-bottom:30px;
}

.chat-box{
    border-radius:10px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)

# ======================================
# HEADER
# ======================================

st.markdown(
    '<p class="main-title">📚 GyanMasti.ai</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="sub-title">Learn Smarter • Revise Faster • Score Better</p>',
    unsafe_allow_html=True
)

# ======================================
# PDF READER
# ======================================

def get_pdf_text(pdf_docs):

    text = ""

    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)

        for page in pdf_reader.pages:
            text += page.extract_text()

    return text

# ======================================
# TEXT CHUNKS
# ======================================

def get_text_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_text(text)

    return chunks

# ======================================
# VECTOR STORE
# ======================================

def get_vector_store(text_chunks):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )

    vector_store = FAISS.from_texts(
        text_chunks,
        embedding=embeddings
    )

    vector_store.save_local("faiss_index")

# ======================================
# PROMPT
# ======================================

def get_conversational_chain():

    prompt_template = """

You are GyanMasti.ai.

Answer the question using only the uploaded study material.

Rules:

1. Use uploaded notes first.
2. If answer not found, say:
   "I could not find this information in the uploaded notes."
3. Explain in easy language.
4. Use bullet points.
5. Mention important exam points.
6. Do not hallucinate.

Context:
{context}

Question:
{question}

Answer:

"""

    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-pro",
        temperature=0.3
    )

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    chain = load_qa_chain(
        model,
        chain_type="stuff",
        prompt=prompt
    )

    return chain

# ======================================
# USER QUESTION
# ======================================

def user_input(user_question):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )

    db = FAISS.load_local(
        "faiss_index",
        embeddings,
        allow_dangerous_deserialization=True
    )

    docs = db.similarity_search(
        user_question,
        k=4
    )

    chain = get_conversational_chain()

    response = chain(
        {
            "input_documents": docs,
            "question": user_question
        },
        return_only_outputs=True
    )

    return response["output_text"]

# ======================================
# CHAT HISTORY
# ======================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ======================================
# SIDEBAR
# ======================================

with st.sidebar:

    st.header("📂 Upload Notes")

    pdf_docs = st.file_uploader(
        "Upload PDFs",
        accept_multiple_files=True
    )

    if st.button("🚀 Process PDFs"):

        with st.spinner("Reading PDFs..."):

            raw_text = get_pdf_text(pdf_docs)

            chunks = get_text_chunks(raw_text)

            get_vector_store(chunks)

        st.success("PDFs Processed Successfully!")

    st.markdown("---")

    st.markdown("""
### Features

✅ Multiple PDFs

✅ Ask Questions

✅ Revision Notes

✅ Exam Preparation

✅ AI Tutor

✅ Chat History

""")

# ======================================
# CHAT DISPLAY
# ======================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ======================================
# USER INPUT
# ======================================

question = st.chat_input(
    "Ask anything from your notes..."
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

        with st.spinner("Thinking..."):

            try:

                answer = user_input(question)

            except:

                answer = """
Please upload and process PDFs first.
"""

            st.markdown(answer)

    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

# ======================================
# FOOTER
# ======================================

st.markdown("---")

st.markdown(
"""
<center>

Made with ❤️ by GyanMasti.ai

</center>
""",
unsafe_allow_html=True
)
