import streamlit as st
import google.generativeai as genai

# =========================
# GEMINI API KEY
# =========================
GEMINI_API_KEY = "AQ.Ab8RN6IJyltp_ScFjnb4m7PNw3vnS5XS8FQu6vKCORUz3sUQmA"

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# PAGE SETTINGS
# =========================
st.set_page_config(
    page_title="GyanMasti.ai",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 GyanMasti.ai")
st.caption("AI Learning Assistant")

# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
You are GyanMasti.ai.

You help students learn from study materials.

Rules:
- Explain concepts in simple language.
- Give examples.
- Generate notes.
- Generate MCQs.
- Be student-friendly.
"""

# =========================
# CHAT HISTORY
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# USER INPUT
# =========================
prompt = st.chat_input("Ask your question...")

if prompt:

    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        response = model.generate_content(
            SYSTEM_PROMPT + "\n\nUser: " + prompt
        )

        answer = response.text

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:
        st.error(f"Error: {e}")
