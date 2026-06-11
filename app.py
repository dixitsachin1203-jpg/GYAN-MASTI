# app.py

```python
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# GEMINI API KEY
# =====================================================

GEMINI_API_KEY = "AQ.Ab8RN6IJyltp_ScFjnb4m7PNw3vnS5XS8FQu6vKCORUz3sUQmA"

# =====================================================
# GEMINI INITIALIZATION
# =====================================================

model = None

if GEMINI_API_KEY.strip():

    try:

        genai.configure(api_key=GEMINI_API_KEY)

        model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    except Exception as e:

        st.sidebar.error(f"Gemini Error: {e}")

# =====================================================
# CUSTOM CSS
# =====================================================

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
margin-bottom:0px;
}

.sub-title{
text-align:center;
font-size:20px;
color:#cbd5e1;
margin-top:0px;
}

.creator{
text-align:center;
color:#38bdf8;
font-size:16px;
margin-bottom:25px;
}

footer{
visibility:hidden;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🎓 GYANMASTI.AI")

    st.markdown("---")

    st.subheader("Study Mode")

    study_mode = st.selectbox(
        "Select Mode",
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

    uploaded_file = st.file_uploader(
        "Upload Study Material",
        type=["pdf", "txt", "docx"]
    )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    if model:
        st.success("🟢 Gemini Connected")
    else:
        st.warning("🟡 Add Gemini API Key")

    st.markdown("---")

    st.info(
        """
        GYANMASTI.AI
        
        Educational AI Assistant
        
        Powered by Gemini
        
        Created by Geetansh Shukla
        """
    )

# =====================================================
# HEADER
# =====================================================

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

# =====================================================
# CHAT HISTORY
# =====================================================

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# CHAT INPUT
# =====================================================

prompt = st.chat_input(
    "Ask GYANMASTI.AI anything..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        if model:

            try:

                response = model.generate_content(
                    f"""
                    You are GYANMASTI.AI,
                    an educational AI assistant.

                    Study Mode:
                    {study_mode}

                    User Question:
                    {prompt}
                    """
                )

                answer = response.text

            except Exception as e:

                answer = f"❌ Gemini Error: {e}"

        else:

            answer = """
🔑 Gemini API Key Required

Open app.py

Find:

GEMINI_API_KEY = ""

Paste your Gemini API key between the quotes.

Restart the application.
"""

        st.markdown(answer)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

# =====================================================
# FOOTER
# =====================================================

st.markdown("---")

current_year = datetime.now().year

st.markdown(
f"""
<center>

### 🎓 GYANMASTI.AI

Learn • Revise • Succeed

Powered by Geetansh Shukla

© {current_year}

</center>
""",
unsafe_allow_html=True
)
```
