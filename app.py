import streamlit as st
import os
from google import genai
from google.genai import types

# -----------------------------------------------------------------------------
# 1. STREAMLIT PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GyanMasti.ai",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS injecting a Cyber-Neon Dark Theme with Glassmorphism
custom_css = """
<style>
    /* Main Background & Fonts */
    .stApp {
        background: linear-gradient(135deg, #0f0c1b 0%, #15102a 50%, #060409 100%);
        color: #e0e0ff;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Animation & Styling */
    .brand-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(45deg, #00f2fe, #4facfe, #9b51e0, #ff007f);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: GradientFlow 6s ease infinite;
        margin-bottom: 0px;
    }
    .brand-subtitle {
        font-size: 1rem;
        color: #8b8ba7;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    @keyframes GradientFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Sidebar Container Glassmorphism */
    section[data-testid="stSidebar"] {
        background: rgba(15, 10, 30, 0.7) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 0, 127, 0.2);
    }

    /* Chat Message Layouts */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin-bottom: 5rem;
    }
    
    .message-row {
        display: flex;
        width: 100%;
        margin-bottom: 0.5rem;
    }
    .message-row.user { justify-content: flex-end; }
    .message-row.assistant { justify-content: flex-start; }

    .message-bubble {
        padding: 1.2rem 1.6rem;
        border-radius: 20px;
        max-width: 75%;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        font-size: 1.05rem;
    }
    
    /* User Bubble: Vibrant Cyber Pink/Purple */
    .user .message-bubble {
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%);
        color: #ffffff;
        border-bottom-right-radius: 2px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Assistant Bubble: Deep Tech Cyan Dark */
    .assistant .message-bubble {
        background: rgba(25, 20, 50, 0.6);
        color: #e2e8f0;
        border-bottom-left-radius: 2px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        backdrop-filter: blur(8px);
    }
    
    /* Footer branding fixes */
    .footer-text {
        text-align: center;
        color: #6b6b83;
        font-size: 0.85rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 1rem;
    }
    
    /* Streamlit Input Customization Override */
    div[data-testid="stChatInput"] textarea {
        background-color: rgba(20, 15, 35, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 242, 254, 0.4) !important;
        border-radius: 12px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. SIDEBAR CONFIGURATION & API KEY SETUP
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe; margin-top:0;'>⚙️ Matrix Control</h2>", unsafe_allow_html=True)
    st.write("Configure your AI core parameters below.")
    
    # API Key retrieval ladder (Secrets -> Environment -> Manual Input)
    default_key = "AQ.Ab8RN6J1VM_voBKmvfsBcVhnsa8kI_ZUZD1hT8a9T2xaoL_UpA"
    if "GEMINI_API_KEY" in st.secrets:
        default_key = st.secrets["GEMINI_API_KEY"]
    elif os.environ.get("GEMINI_API_KEY"):
        default_key = os.environ.get("GEMINI_API_KEY")
        
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=default_key,
        type="password",
        placeholder="AIzaSy...",
        help="Provide your Gemini API key from Google AI Studio. Left empty, it pulls from st.secrets."
    )
    
    st.markdown("---")
    st.markdown("<h3 style='color:#ff007f;'>🤖 Core Adjustments</h3>", unsafe_allow_html=True)
    
    # Model Selection using modern Google GenAI supported models
    model_choice = st.selectbox(
        "Select Model Variant",
        ["gemini-2.5-flash", "gemini-2.5-pro"],
        index=0,
        help="Flash is lightning fast for conversations. Pro handles advanced logical reasoning."
    )
    
    # Hyperparameters
    creativity = st.slider("Creativity (Temperature)", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
    
    # System Instruction setup to establish the core identity
    system_instruction = (
        "You are GyanMasti.ai, an elite, highly intelligent, and universally capable AI model. "
        "You are proudly designed and powered by your creator, Geetansh Shukla. "
        "Maintain an engaging, brilliantly smart, helpful, and energetic tone. "
        "Acknowledge your structural creation by Geetansh Shukla whenever appropriately asked."
    )
    
    st.markdown("---")
    st.markdown(
        "<div style='color: #8b8ba7; font-size:0.8rem; text-align:center;'>"
        "GyanMasti.ai Engine v2.5<br>© 2026 All Rights Reserved"
        "</div>", 
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 3. CHAT INTERFACE & SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
# Header Display
st.markdown("<h1 class='brand-title'>GyanMasti.ai</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>⚡ Powered by Geetansh Shukla</p>", unsafe_allow_html=True)

# Initialize message history tracking if not present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to the future. I am GyanMasti.ai, engineered by Geetansh Shukla. How can I assist your intellect today?"}
    ]

# Render existing chat history wrapped inside beautifully stylized CSS structural divs
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(
        f'<div class="message-row {role_class}">'
        f'<div class="message-bubble">{msg["content"]}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. ENGINE QUERY & RESPONSE GENERATION
# -----------------------------------------------------------------------------
# Standardised Chat Input box placement
if user_query := st.chat_input("Inquire anything from GyanMasti.ai..."):
    
    # Instantly render user query onto the screen
    st.markdown(
        f'<div class="message-row user">'
        f'<div class="message-bubble">{user_query}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    # Verify API Key Presence before proceeding to call the Google API endpoint
    if not api_key_input:
        st.error("⚠️ Security Authentication Missing: Please provide a Google Gemini API Key in the Matrix sidebar control panel to wake up GyanMasti.ai.")
    else:
        try:
            # Initialize official Client instance using google-genai
            client = genai.Client(api_key=api_key_input)
            
            # Format chat history to match standard Type schema expected by GenAI Client
            formatted_contents = []
            for m in st.session_state.messages:
                # Map roles correctly to 'user' and 'model'
                api_role = "user" if m["role"] == "user" else "model"
                formatted_contents.append(
                    types.Content(
                        role=api_role,
                        parts=[types.Part.from_text(text=m["content"])]
                    )
                )
            
            # Request response chunk stream tracking with integrated system instructions 
            with st.spinner("⚡ GyanMasti.ai is processing..."):
                response_stream = client.models.generate_content_stream(
                    model=model_choice,
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=creativity,
                    ),
                )
                
                # Assemble streaming text updates cleanly
                assistant_response = ""
                # Create a placeholder box to display response chunks dynamically
                response_placeholder = st.empty()
                
                for chunk in response_stream:
                    if chunk.text:
                        assistant_response += chunk.text
                        response_placeholder.markdown(
                            f'<div class="message-row assistant">'
                            f'<div class="message-bubble">{assistant_response}🧭</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                
                # Render clean finalized text without loading cursor emoji
                response_placeholder.markdown(
                    f'<div class="message-row assistant">'
