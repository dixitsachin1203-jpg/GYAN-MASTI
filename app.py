import streamlit as st
import google.generativeai as genai

# ==========================================
# CONFIG
# ==========================================

st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# GEMINI API CONFIG
# ==========================================

API_KEY = "AQ.Ab8RN6JHzZL_xKV_RdnMufeK5uGtm3vZ-sbRpv7mgAbH-87E_Q"

if API_KEY != "AQ.Ab8RN6JHzZL_xKV_RdnMufeK5uGtm3vZ-sbRpv7mgAbH-87E_Q":
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-pro")
else:
    model = None

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
    color:white;
}

.main-title{
    text-align:center;
    font-size:60px;
    font-weight:bold;
    color:white;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:#94a3b8;
}

.powered{
    text-align:center;
    color:#38bdf8;
    font-size:15px;
    margin-bottom:25px;
}

footer {
    visibility:hidden;
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

    st.title("⚙️ GYANMASTI Control")

    st.markdown("---")

    st.subheader("Model")

    st.success("Gemini 2.5 Pro")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.info("""
GYANMASTI.AI

Educational AI Assistant

Powered by Gemini
""")

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
    '<div class="powered">⚡ Powered by Geetansh Shukla</div>',
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

prompt = st.chat_input("Ask anything...")

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

        message_placeholder = st.empty()

        try:

            if model:

                response = model.generate_content(prompt)

                answer = response.text

            else:

                answer = """
🔑 Gemini API Key Not Added Yet

Open app.py and replace:

YOUR_GEMINI_API_KEY_HERE

with your actual Gemini API key.
"""

            message_placeholder.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer
                }
            )

        except Exception as e:

            error_message = f"❌ Error: {str(e)}"

            message_placeholder.error(error_message)

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown(
"""
<center>

### 🎓 GYANMASTI.AI

Powered by Geetansh Shukla

© 2026 All Rights Reserved

</center>
""",
unsafe_allow_html=True
)
