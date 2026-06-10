import streamlit as st
import time
import random

# 1. Page Configuration
st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="collapsed" # Kept clean by default
)

# 2. Inject Custom CSS for Advanced UI/UX & Aesthetics
st.markdown("""
    <style>
    /* Main Background & Font Styling */
    @import url('https://googleapis.com');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #0E1117;
    }
    
    /* Elegant Title Glow Gradient */
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
    
    /* Clean Cards for Prompt Hints */
    .hint-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .hint-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #852DF4;
        transform: translateY(-2px);
    }
    
    /* Chat bubbles redesign tweaks */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 10px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0A0C10;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Custom divider line */
    .glow-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(133, 45, 244, 0.3), transparent);
        margin: 25px 0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Layout (For Configuration Controls)
with st.sidebar:
    st.markdown("### ⚙️ Engine Settings")
    ai_tone = st.select_slider(
        "Model Persona",
        options=["Creative", "Balanced", "Precise"],
        value="Balanced"
    )
    
    st.markdown("---")
    st.markdown("### 🧬 Developer Info")
    st.markdown("**Creator:** Geetansh Shukla")
    st.markdown("**Status:** UI/UX Prototype")
    
    if st.button("🧹 Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 4. Custom App Header & Branding (HTML + CSS Engine)
st.markdown('<h1 class="title-gradient">GYANMASTI.AI</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle-text">⚡ Powered by Geetansh Shukla</p>', unsafe_allow_html=True)

# 5. Initialize Memory Store
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Welcome Banner & Pre-built Hints (UX element to reduce user typing effort)
if len(st.session_state.messages) == 0:
    st.markdown("""
    <div style='background: rgba(133, 45, 244, 0.1); border-left: 4px solid #852DF4; padding: 15px; border-radius: 4px; margin-bottom: 25px;'>
        ✨ <strong>Welcome to the Future!</strong> GYANMASTI.AI interface is ready. Type a prompt below or use one of the aesthetic quick-start templates to test the simulated engine.
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### 💡 Quick Start Templates")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🚀 Explain Quantum Physics in simple terms", use_container_width=True):
            st.session_state.active_prompt = "Explain Quantum Physics in simple terms"
            
        if st.button("📝 Write a catchy marketing slogan for a tech brand", use_container_width=True):
            st.session_state.active_prompt = "Write a catchy marketing slogan for a tech brand"
            
    with col2:
        if st.button("💻 Debug a Python loops efficiency problem", use_container_width=True):
            st.session_state.active_prompt = "Debug a Python loops efficiency problem"
            
        if st.button("🎨 Suggest a stunning color palette for an AI app", use_container_width=True):
            st.session_state.active_prompt = "Suggest a stunning color palette for an AI app"

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# Mock Answers Engine
MOCK_LIBRARY = {
    "Creative": "Your creative spark is ready! Under this mode, I will formulate answers rich in vocabulary, vivid analogies, and unique out-of-the-box system concepts. When Geetansh binds my live API, I'll build worlds for you!",
    "Balanced": "Processing logic standard. Striking the perfect equilibrium between technical accuracy and everyday human-understandable conversation. This is the optimal mode for production workflows.",
    "Precise": "Fact-check sequence initiated. Prioritizing structured tables, itemized bullet points, micro-precision data parameters, and objective breakdowns. Zero conversational filler included."
}

# 7. Render Chat Feed
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 8. Interactive Prompt Trigger Handler
# Detect if user clicked on any Quick Template buttons
default_input = ""
if "active_prompt" in st.session_state and st.session_state.active_prompt:
    default_input = st.session_state.active_prompt
    st.session_state.active_prompt = None # Clear it immediately

# 9. Main User Chat Field
if user_query := st.chat_input("Message GYANMASTI.AI...", key="chat_box"):
    # If standard text box input came through, execute it
    current_prompt = user_query
elif default_input:
    # If a button template was clicked, execute it instead
    current_prompt = default_input
else:
    current_prompt = None

if current_prompt:
    # Render user query instantly
    with st.chat_message("user"):
        st.markdown(current_prompt)
    st.session_state.messages.append({"role": "user", "content": current_prompt})

    # Render simulated assistant response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Pull response based on mode
        body_text = MOCK_LIBRARY[ai_tone]
        full_response = f"✨ **[Mode: {ai_tone}]**\n\nYou asked: *\"{current_prompt}\"*\n\nHere is my aesthetic sample output: {body_text}"
        
        # Word-by-word premium stream effect animation
        displayed_text = ""
        for word in full_response.split(" "):
            displayed_text += word + " "
            time.sleep(0.04)  # Natural flowing smooth delay
            response_placeholder.markdown(displayed_text + "▒")
            
        # Final clean render
        response_placeholder.markdown(displayed_text)
        
    # Append to state history
    st.session_state.messages.append({"role": "assistant", "content": displayed_text})
    st.rerun() # Clean update to wipe old prompt flags
