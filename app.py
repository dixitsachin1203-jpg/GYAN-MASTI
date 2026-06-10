import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Inject Premium Dark Theme Aesthetics
st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
    }
    
    .title-gradient {
        background: linear-gradient(90deg, #FF4B4B, #852DF4, #4A00E0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem !important;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
        padding-bottom: 0px;
        letter-spacing: -1px;
    }
    
    .subtitle-text {
        text-align: center;
        color: #A0AEC0;
        font-size: 1.1rem;
        margin-top: -10px;
        margin-bottom: 30px;
        font-weight: 300;
    }
    
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 10px;
    }
    
    [data-testid="stSidebar"] {
        background-color: #0A0C10;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(133, 45, 244, 0.3), transparent);
        margin: 25px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Secure Production API Key Configuration
API_KEY = "AQ.Ab8RN6LrJWF71BqNTDthIzwnBmOrOVJt8s7FAcjXLluCV7x7IA"
genai.configure(api_key=API_KEY)

# 4. Reference your trained model path
MODEL_PATH = "tunedModels/gyanmasti-core-v1"

# 5. Sidebar Layout Panel
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    st.info("Model Identity: Fine-Tuned Active ✅")
    st.markdown("---")
    st.markdown("### 🧬 Developer Info")
    st.markdown("**Creator:** Geetansh Shukla")
    
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 6. Main Branding Header
st.markdown('<h1 class="title-gradient">GYANMASTI.AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">⚡ Powered by Geetansh Shukla</p>', unsafe_allow_html=True)

# 7. Initialize Memory Store
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Start Templates
if len(st.session_state.messages) == 0:
    st.markdown("#### 💡 Test Your Training")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧠 Who created GYANMASTI.AI?", use_container_width=True):
            st.session_state.active_prompt = "Who created GYANMASTI.AI?"
    with col2:
        if st.button("🚀 Who is Geetansh Shukla?", use_container_width=True):
            st.session_state.active_prompt = "Who is Geetansh Shukla?"

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# 8. Render Chat Feed
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 9. Handle Prompt Selections
default_input = ""
if "active_prompt" in st.session_state and st.session_state.active_prompt:
    default_input = st.session_state.active_prompt
    st.session_state.active_prompt = None

if user_query := st.chat_input("Message GYANMASTI.AI..."):
    current_prompt = user_query
elif default_input:
    current_prompt = default_input
else:
    current_prompt = None

# 10. API Execution Pipeline
if current_prompt:
    with st.chat_message("user"):
        st.markdown(current_prompt)
    st.session_state.messages.append({"role": "user", "content": current_prompt})

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        try:
            # Reconstruct the session history structure for the chat engine
            chat = genai.GenerativeModel(model_name=MODEL_PATH).start_chat(history=[])
            
            # Request response text directly from your custom brain
            response = chat.send_message(current_prompt)
            
            response_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            st.rerun()
            
        except Exception as e:
            response_placeholder.error(f"Engine connection failed: {str(e)}")
