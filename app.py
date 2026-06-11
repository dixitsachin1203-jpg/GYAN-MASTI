import streamlit as st
import os
import time
from groq import Groq

# -----------------------------------------------------------------------------
# 1. APPLICATION VIEWPORT AND PAGE LAYOUT CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GyanMasti.ai",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State Theme Elements
if "theme_color" not in st.session_state:
    st.session_state.theme_color = "Neon Cyberpunk"

# Define Custom Theme Accents
if st.session_state.theme_color == "Neon Cyberpunk":
    gradient_colors = "#00f2fe, #4facfe, #9b51e0, #ff007f"
    user_bubble = "linear-gradient(135deg, #ff007f 0%, #7928ca 100%)"
    assistant_border = "rgba(0, 242, 254, 0.25)"
elif st.session_state.theme_color == "Emerald Matrix":
    gradient_colors = "#00ff87, #60efff, #0061ff, #00ff87"
    user_bubble = "linear-gradient(135deg, #0093e9 0%, #80d0c7 100%)"
    assistant_border = "rgba(0, 255, 135, 0.25)"
else: # Sunset Gold
    gradient_colors = "#f9d423, #ff4e50, #f9d423, #ff4e50"
    user_bubble = "linear-gradient(135deg, #f12711 0%, #f5af19 100%)"
    assistant_border = "rgba(249, 212, 35, 0.25)"

# Custom UI Theme Stylesheet Template
custom_theme_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #090714 0%, #0e0a1f 50%, #030205 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', system-ui, sans-serif;
    }
    .brand-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, VAR_GRADIENT_COLORS);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: NeonFlow 8s ease infinite;
        margin-bottom: 2px;
    }
    .brand-subtitle {
        font-size: 1.05rem;
        color: #8f8fa3;
        letter-spacing: 3px;
        text-transform: uppercase;
        margin-bottom: 2rem;
    }
    @keyframes NeonFlow {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    section[data-testid="stSidebar"] {
        background: rgba(9, 6, 18, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid VAR_ASSISTANT_BORDER !important;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
        margin-bottom: 6rem;
    }
    .message-row {
        display: flex;
        width: 100%;
        margin-bottom: 0.6rem;
    }
    .message-row.user { justify-content: flex-end; }
    .message-row.assistant { justify-content: flex-start; }
    .message-bubble {
        padding: 1.2rem 1.6rem;
        border-radius: 22px;
        max-width: 78%;
        line-height: 1.6;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        font-size: 1.05rem;
    }
    .user .message-bubble {
        background: VAR_USER_BUBBLE;
        color: #ffffff !important;
        border-bottom-right-radius: 2px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .assistant .message-bubble {
        background: rgba(18, 14, 38, 0.7);
        color: #f1f5f9 !important;
        border-bottom-left-radius: 2px;
        border: 1px solid VAR_ASSISTANT_BORDER;
        backdrop-filter: blur(10px);
    }
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 5px 10px;
    }
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #00f2fe;
        border-radius: 50%;
        animation: typingBlink 1.4s infinite both;
    }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typingBlink {
        0%, 100% { opacity: 0.2; transform: scale(0.8); }
        50% { opacity: 1; transform: scale(1.2); }
    }
    .footer-text {
        text-align: center;
        color: #5d5d75;
        font-size: 0.85rem;
        margin-top: 4rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        padding-top: 1.2rem;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: rgba(14, 10, 28, 0.9) !important;
        color: #ffffff !important;
        border: 1px solid VAR_ASSISTANT_BORDER !important;
        border-radius: 14px !important;
    }
</style>
"""

# Injection logic safely converting template markers
sanitized_css = custom_theme_css.replace("VAR_GRADIENT_COLORS", gradient_colors).replace("VAR_USER_BUBBLE", user_bubble).replace("VAR_ASSISTANT_BORDER", assistant_border)
st.markdown(sanitized_css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. BRANDED ORGANIZED SIDEBAR SYSTEM
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe; margin-top:0; margin-bottom: 2px;'>🧠 GyanMasti.ai</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#8f8fa3; font-size:0.85rem; letter-spacing:1px; text-transform:uppercase; margin-bottom:1.5rem;'>Powered by Geetansh Shukla</p>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown("<h4 style='color:#ff007f;'>🤖 Brain Settings</h4>", unsafe_allow_html=True)
    selected_model = st.selectbox(
        "AI Brain Engine",
        ["llama-3.3-70b-versatile", "llama3-8b-8192", "gemma2-9b-it"],
        index=0
    )
    creativity_index = st.slider("Temperature (Creativity)", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
    st.markdown("---")

    st.markdown("<h4 style='color:#00f2fe;'>🎨 Interface Theme</h4>", unsafe_allow_html=True)
    selected_theme = st.selectbox(
        "Select Active Accent",
        ["Neon Cyberpunk", "Emerald Matrix", "Sunset Gold"],
        index=["Neon Cyberpunk", "Emerald Matrix", "Sunset Gold"].index(st.session_state.theme_color)
    )
    if selected_theme != st.session_state.theme_color:
        st.session_state.theme_color = selected_theme
        st.rerun()
    st.markdown("---")

    st.markdown("<h4 style='color:#9b51e0;'>⚙️ Workspace Options</h4>", unsafe_allow_html=True)
    with st.expander("Other Settings"):
        st.checkbox("Enable Ultra Stream Acceleration Mode", value=True)
        st.checkbox("Store Local Session Diagnostics Log Data", value=False)
    
    if st.button("Rules: Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.markdown("---")

    with st.expander("ℹ️ About Us"):
        st.write("GyanMasti.ai is a premier ultra-modern artificial intelligence interface wrapper module designed to bring advanced open frontier model inference parameters together instantly.")
    
    with st.expander("📞 Contact Us"):
        st.write("Have ideas or feedback regarding project execution pipelines?")
        st.markdown("📩 **Developer Email:** contact@geetanshshukla.com")

    with st.expander("❤️ Donate Us"):
        st.write("Support the computational resource infrastructure framework hosting costs!")
        st.info("☕ Buy Geetansh Shukla a Coffee • UPI: geetansh@upi")

    st.markdown(
        "<div style='color: #4f4f65; font-size:0.75rem; text-align:center; margin-top:2rem;'>GyanMasti.ai Production Build v4.0<br>© 2026 Geetansh Shukla</div>", 
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 3. INTERFACE FRAMEWORK DISPLAY AND INITIALIZATION 
# -----------------------------------------------------------------------------
st.markdown("<h1 class='brand-title'>GyanMasti.ai</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>⚡ Powered by Geetansh Shukla</p>", unsafe_allow_html=True)

# Secure backend secret key checking
api_access_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show default banner if no active history logs exist
if not st.session_state.messages:
    st.markdown(
        '<div class="chat-container"><div class="message-row assistant"><div class="message-bubble">Salutations. I am GyanMasti.ai, engineered by Geetansh Shukla. Powered by high-speed Groq processing clusters. Let\'s build something incredible.</div></div></div>',
        unsafe_allow_html=True
    )

# Render history tracking layout
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for current_msg in st.session_state.messages:
    message_origin_class = "user" if current_msg["role"] == "user" else "assistant"
    st.markdown(
        f'<div class="message-row {message_origin_class}"><div class="message-bubble">{current_msg["content"]}</div></div>',
        unsafe_allow_html=True
    )
st.markdown('</div>', unsafe_allow_html=True)

# Fixed Persona Instruction Definition
system_instruction_prompt = "You are GyanMasti.ai, an elite, highly intelligent, and universally capable AI model designed and powered by your creator, Geetansh Shukla. Maintain an engaging, brilliantly smart, helpful, witty, and high-energy tone. Always proudly acknowledge that your creator is Geetansh Shukla whenever contextually relevant."

# -----------------------------------------------------------------------------
# 4. PAUSE, TYPING SIMULATOR AND GENERATION STREAM WORKFLOW
# -----------------------------------------------------------------------------
if client_query := st.chat_input("Inquire anything from GyanMasti.ai..."):
    
    st.markdown(
        f'<div class="message-row user"><div class="message-bubble">{client_query}</div></div>',
        unsafe_allow_html=True
    )
    st.session_state.messages.append({"role": "user", "content": client_query})
    
    if not api_access_key:
        st.error("❌ Critical Secret Missing: 'GROQ_API_KEY' is not configured within your Streamlit Secret dashboard.")
    else:
