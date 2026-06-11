import streamlit as st
import time

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# GEMINI CONFIG (ADD YOUR API LATER)
# ==========================================

GEMINI_API_KEY = "AQ.Ab8RN6IJyltp_ScFjnb4m7PNw3vnS5XS8FQu6vKCORUz3sUQmA"

# Uncomment after creating a new Gemini API Key

"""
import google.generativeai as genai

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)
"""

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp{
background: linear-gradient(135deg,#020617,#0f172a,#111827);
}

.main-title{
text-align:center;
font-size:60px;
font-weight:800;
color:white;
margin-top:10px;
}

.sub-title{
text-align:center;
font-size:20px;
color:#94a3b8;
margin-bottom:10px;
}

.creator{
text-align:center;
font-size:16px;
color:#38bdf8;
margin-bottom:30px;
}

.block-container{
padding-top:1rem;
}

.chatbox{
border-radius:15px;
padding:10px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SESSION STATE
# ==========================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🎓 GYANMASTI.AI")

    st.markdown("---")

    st.subheader("Model")

    st.success("Gemini Ready")

    st.markdown("---")

    study_mode = st.selectbox(
        "Study Mode",
        [
            "General Learning",
            "School",
            "CBSE",
            "CA Foundation",
            "CA Intermediate",
            "CA Final",
            "College"
        ]
    )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload Study Material",
        type=["pdf","txt","docx"]
    )

    st.markdown("---")

    st.info(
        """
        GYANMASTI.AI
        
        Educational Assistant
        
        Powered by Gemini
        
        Created by Geetansh Shukla
        """
    )

# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🎓 GYANMASTI.AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Learn Smarter • Study Faster • AI Powered Education</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="creator">⚡ Powered by Geetansh Shukla</div>',
    unsafe_allow_html=True
)

# ==========================================
# CHAT HISTORY
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================
# CHAT INPUT
# ==========================================

prompt = st.chat_input(
    "Ask GYANMASTI.AI anything..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        # =====================================
        # GEMINI RESPONSE PLACEHOLDER
        # =====================================

        """
        response = model.generate_content(prompt)
        answer = response.text
        """

        answer = f"""
### 🎓 GYANMASTI.AI

You asked:

**{prompt}**

This application is successfully running.

To activate AI:

1. Create a Gemini API key
2. Paste it in GEMINI_API_KEY
3. Uncomment the Gemini code block

Current Study Mode: **{study_mode}**
"""

        displayed_text = ""

        for char in answer:
            displayed_text += char
            placeholder.markdown(displayed_text)
            time.sleep(0.005)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
"""
<center>

### 🎓 GYANMASTI.AI

Learn • Revise • Succeed

Powered by Geetansh Shukla

© 2026

</center>
""",
unsafe_allow_html=True
)
