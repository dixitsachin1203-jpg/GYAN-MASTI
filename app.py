import streamlit as st
from google import genai
from google.genai import types

# 1. Page Configuration
st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Inject Premium CSS Styling & Theme
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

# 3. Secure Key Configuration (Hardcoded for your local system run)
# PASTE YOUR API KEY INSIDE THE QUOTES BELOW ON YOUR COMPUTER:
GEMINI_API_KEY = "YOUR_API_KEY_HERE"

# 4. Sidebar Controls
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    ai_tone = st.select_slider(
        "Model Persona",
        options=["Creative", "Balanced", "Precise"],
        value="Balanced"
    )
    
    # Map visual settings to actual temperature numbers
    temp_mapping = {"Creative": 1.0, "Balanced": 0.7, "Precise": 0.2}
    current_temp = temp_mapping[ai_tone]
    
    st.markdown("---")
    st.markdown("### 🧬 Developer Info")
    st.markdown("**Creator:** Geetansh Shukla")
    st.markdown("**Status:** Production Live 🚀")
    
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 5. Application Header
st.markdown('<h1 class="title-gradient">GYANMASTI.AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">⚡ Powered by Geetansh Shukla</p>', unsafe_allow_html=True)

# 6. Session States Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Quick Start Templates (Hidden if context history exists)
if len(st.session_state.messages) == 0:
    st.markdown("#### 💡 Quick Start Templates")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Explain Quantum Physics simply", use_container_width=True):
            st.session_state.active_prompt = "Explain Quantum Physics in simple terms"
        if st.button("📝 Write a tech brand slogan", use_container_width=True):
            st.session_state.active_prompt = "Write a catchy marketing slogan for a tech brand"
    with col2:
        if st.button("💻 Optimize a Python loop structure", use_container_width=True):
            st.session_state.active_prompt = "Debug a Python loops efficiency problem"
        if st.button("🎨 Design an AI app color palette", use_container_width=True):
            st.session_state.active_prompt = "Suggest a stunning color palette for an AI app"

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# 7. Render History Feed
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Input Trigger Handler
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

# 9. Real API Inference Execution
if current_prompt:
    # Display human chat block
    with st.chat_message("user"):
        st.markdown(current_prompt)
    st.session_state.messages.append({"role": "user", "content": current_prompt})

    # Display system response streaming block
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        if GEMINI_API_KEY == "YOUR_API_KEY_HERE":
            response_placeholder.error("Configuration Required: Please paste your API key inside the script's `GEMINI_API_KEY` variable to unlock production capabilities.")
        else:
            try:
                # Setup client and parse context history structure
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                gemini_history = []
                for msg in st.session_state.messages[:-1]:
                    gemini_history.append(
                        types.Content(
                            role="user" if msg["role"] == "user" else "model",
                            parts=[types.Part.from_text(text=msg["content"])]
                        )
                    )
                
                # Active session pipeline using stable gemini-2.5-flash
                chat = client.chats.create(
                    model="gemini-2.5-flash",
                    history=gemini_history,
                    config=types.GenerateContentConfig(temperature=current_temp)
                )
                
                # Fetch text response directly from target
                response = chat.send_message(current_prompt)
                
                # Render clean output Markdown text 
                response_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.rerun()
                
            except Exception as e:
                response_placeholder.error(f"Engine connection failed: {str(e)}")
