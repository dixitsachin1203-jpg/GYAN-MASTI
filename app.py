import streamlit as st
from google import genai
from google.genai import types
import os
import time

# Set page configuration
st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hardcoded Default API Key provided by user
DEFAULT_API_KEY = "AQ.Ab8RN6IYxCJ6776e9H95b2VilQz69KYBl9F_VSvlpea5gvsbhg"

# Custom System Instruction for model persona
SYSTEM_INSTRUCTION = (
    "You are GYANMASTI.AI, a premium AI platform designed and developed by Geetansh Shukla. "
    "Under no circumstances should you state that you were built by Google, OpenAI, Meta, or any other team. "
    "If the user asks who created you or made you or developed you, you must say: "
    "'I am GYANMASTI.AI, a premium AI platform designed and developed by Geetansh Shukla.' "
    "If the user asks what GYANMASTI.AI is, you must say: "
    "'GYANMASTI.AI is an advanced conversational platform powered by state-of-the-art Google Gemini models, "
    "crafted to deliver a superior user experience and intelligent answers.' "
    "If the user asks about Geetansh Shukla, you must say: "
    "'Geetansh Shukla is the visionary creator, developer, and innovator behind GYANMASTI.AI, "
    "dedicated to building high-utility, beautifully designed AI systems.' "
    "Make sure to keep this persona throughout the entire conversation, responding in a helpful, knowledgeable, "
    "and professional tone."
)

# Custom themes dictionary with distinct gradients and border colors
THEMES = {
    "Midnight Nebula 🌌": {
        "bg": "linear-gradient(135deg, #070913 0%, #0F172A 100%)",
        "accent": "linear-gradient(135deg, #3B82F6 0%, #A855F7 100%)",
        "border": "rgba(168, 85, 247, 0.2)",
        "shadow": "rgba(168, 85, 247, 0.08)",
        "user_bg": "linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.15) 100%)",
        "user_border": "rgba(59, 130, 246, 0.2)"
    },
    "Cyberpunk Glow ⚡": {
        "bg": "linear-gradient(135deg, #0A0518 0%, #1A0D36 100%)",
        "accent": "linear-gradient(135deg, #06B6D4 0%, #EC4899 100%)",
        "border": "rgba(236, 72, 153, 0.25)",
        "shadow": "rgba(236, 72, 153, 0.1)",
        "user_bg": "linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(236, 72, 153, 0.15) 100%)",
        "user_border": "rgba(6, 182, 212, 0.25)"
    },
    "Emerald Forest 🍃": {
        "bg": "linear-gradient(135deg, #041007 0%, #0A2411 100%)",
        "accent": "linear-gradient(135deg, #10B981 0%, #F59E0B 100%)",
        "border": "rgba(245, 158, 11, 0.2)",
        "shadow": "rgba(245, 158, 11, 0.08)",
        "user_bg": "linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(245, 158, 11, 0.15) 100%)",
        "user_border": "rgba(16, 185, 129, 0.2)"
    },
    "Sunset Horizon 🌅": {
        "bg": "linear-gradient(135deg, #180505 0%, #2D0F0F 100%)",
        "accent": "linear-gradient(135deg, #EF4444 0%, #F59E0B 100%)",
        "border": "rgba(245, 158, 11, 0.2)",
        "shadow": "rgba(245, 158, 11, 0.08)",
        "user_bg": "linear-gradient(135deg, rgba(239, 68, 68, 0.08) 0%, rgba(245, 158, 11, 0.15) 100%)",
        "user_border": "rgba(239, 68, 68, 0.2)"
    }
}

# Simulated chat history database with pre-configured questions and answers
HISTORY_DEMO = {
    "⚡ UI/UX Optimization Checklist": [
        {"role": "user", "content": "How do I optimize the UI/UX of a dashboard?"},
        {"role": "assistant", "content": "To optimize a dashboard for the ultimate user experience:\n1. **Use glassmorphism** for panels to create depth.\n2. **Incorporate custom gradients** instead of flat solid colors.\n3. **Use a single font family** with strong weight variation (like `Outfit`).\n4. **Add micro-animations** on button hover to make the UI feel alive."}
    ],
    "🎨 Premium Glassmorphism Guide": [
        {"role": "user", "content": "Give me a CSS snippet for a premium glassmorphic card."},
        {"role": "assistant", "content": "Here is a premium glassmorphic CSS snippet:\n```css\n.card {\n    background: rgba(255, 255, 255, 0.03);\n    backdrop-filter: blur(12px);\n    border: 1px solid rgba(255, 255, 255, 0.06);\n    border-radius: 16px;\n    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);\n}\n```"}
    ],
    "🤖 Gemini Integration Sandbox": [
        {"role": "user", "content": "How do I stream responses in google-generativeai?"},
        {"role": "assistant", "content": "You can stream responses by calling `model.generate_content(prompt, stream=True)` and iterating over the response chunks:\n```python\nresponse = model.generate_content(prompt, stream=True)\nfor chunk in response:\n    print(chunk.text)\n```"}
    ]
}

def inject_custom_css(theme):
    """Inject premium CSS styling into Streamlit to deliver an elite UI/UX experience."""
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Apply fonts and base dark gradient theme globally */
        html, body, [class*="css"], .stApp {{
            font-family: 'Outfit', 'Inter', sans-serif !important;
            background: {theme['bg']} !important;
            color: #F8FAFC !important;
        }}
        
        /* Sidebar layout and border styling */
        section[data-testid="stSidebar"] {{
            background-color: #06080E !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }}
        
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
            padding-top: 1.5rem;
        }}
        
        /* Sidebar Expander styling */
        .streamlit-expanderHeader {{
            background-color: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            font-size: 0.95rem !important;
            color: #F8FAFC !important;
            margin-bottom: 5px;
        }}
        
        /* Text styling with active theme gradient */
        .gradient-text {{
            background: {theme['accent']};
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        
        /* Custom Chat bubble styles */
        div[data-testid="stChatMessage"] {{
            background-color: rgba(15, 23, 42, 0.45) !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            border-radius: 16px !important;
            padding: 16px 20px !important;
            margin-bottom: 14px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        div[data-testid="stChatMessage"]:hover {{
            border-color: {theme['border']} !important;
            box-shadow: 0 10px 30px {theme['shadow']} !important;
            transform: translateY(-2px);
        }}
        
        .user-bubble {{
            background: {theme['user_bg']};
            border: 1px solid {theme['user_border']} !important;
            border-radius: 14px;
            padding: 12px 16px;
            color: #F8FAFC;
            font-size: 1rem;
            line-height: 1.5;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }}
        
        /* Premium code formatting styling */
        code {{
            background-color: rgba(255, 255, 255, 0.06) !important;
            border-radius: 6px !important;
            padding: 2px 6px !important;
            font-family: 'Courier New', Courier, monospace !important;
            color: #F472B6 !important;
        }}
        pre code {{
            background-color: rgba(0, 0, 0, 0.25) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            padding: 14px !important;
            border-radius: 12px !important;
            display: block !important;
            overflow-x: auto !important;
            color: #E2E8F0 !important;
        }}
        
        /* Sidebar New Chat Button styling (first button) */
        div[data-testid="stSidebar"] button:first-of-type {{
            background: {theme['accent']} !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 20px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.2) !important;
        }}
        
        div[data-testid="stSidebar"] button:first-of-type:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(59, 130, 246, 0.45) !important;
            color: white !important;
        }}
        
        /* Sidebar Chat History list items styling (subsequent buttons) */
        div[data-testid="stSidebar"] button:not(:first-of-type) {{
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            border-radius: 10px !important;
            color: #CBD5E1 !important;
            text-align: left !important;
            padding: 10px 14px !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            box-shadow: none !important;
            margin-bottom: 8px !important;
            justify-content: flex-start !important;
            transition: all 0.2s ease !important;
            white-space: normal !important;
            word-wrap: break-word !important;
        }}
        
        div[data-testid="stSidebar"] button:not(:first-of-type):hover {{
            background: rgba(255, 255, 255, 0.06) !important;
            border-color: rgba(255, 255, 255, 0.1) !important;
            color: #F8FAFC !important;
            transform: scale(1.02) !important;
        }}
        
        /* Glassmorphic Preset Prompt Cards */
        .welcome-container .stButton > button {{
            background: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 16px !important;
            color: #E2E8F0 !important;
            padding: 24px 20px !important;
            text-align: left !important;
            font-size: 0.95rem !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            min-height: 110px !important;
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
            backdrop-filter: blur(8px);
            white-space: normal !important;
            word-wrap: break-word !important;
        }}
        
        .welcome-container .stButton > button:hover {{
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%) !important;
            border-color: {theme['border']} !important;
            transform: translateY(-4px) !important;
            box-shadow: 0 10px 25px -5px {theme['shadow']} !important;
            color: #FFFFFF !important;
        }}
        
        /* Chat Input field alignment and float styling */
        div[data-testid="stChatInput"] {{
            border-radius: 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            background-color: rgba(10, 15, 30, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.3) !important;
            padding: 6px 14px !important;
        }}
        
        div[data-testid="stChatInput"] textarea {{
            color: #F8FAFC !important;
        }}
        
        /* Hiding core Streamlit branding headers and footers, preserving sidebar toggle */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header[data-testid="stHeader"] {{
            background: transparent !important;
        }}
        div[data-testid="stDecorator"],
        div[data-testid="stHeaderDeployButton"],
        button[data-testid="stHeaderMenuButton"] {{
            display: none !important;
        }}
        
        /* Glowing Hero Banner */
        .hero-banner {{
            background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.08), transparent 45%),
                        radial-gradient(circle at bottom right, rgba(139, 92, 246, 0.08), transparent 45%);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 24px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }}
        
        /* Sidebar footer styling */
        .sidebar-footer {{
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
        }}
        
        /* Loading Dot Pulse Animation */
        .glowing-loader {{
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px 0;
        }}
        .loader-dot {{
            width: 10px;
            height: 10px;
            margin: 0 6px;
            border-radius: 50%;
            background: {theme['accent']};
            animation: bounce 0.6s infinite alternate;
        }}
        .loader-dot:nth-child(2) {{ animation-delay: 0.2s; }}
        .loader-dot:nth-child(3) {{ animation-delay: 0.4s; }}
        
        @keyframes bounce {{
            to {{ transform: translateY(-10px); }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def check_creator_dataset(prompt: str) -> str:
    """Interceptors to handle creator and brand queries natively using predefined answers."""
    cleaned = prompt.strip().lower().rstrip("?.").strip()
    
    # Predefined creator queries
    creator_questions = [
        "who made you", 
        "who is your creator", 
        "who developed you",
        "who created you",
        "who built you",
        "who designed you",
        "who is the creator of gyanmasti",
        "who is the developer of gyanmasti"
    ]
    if any(q in cleaned for q in creator_questions):
        return "I am GYANMASTI.AI, a premium AI platform designed and developed by Geetansh Shukla."
        
    # Predefined platform queries
    platform_questions = [
        "what is gyanmastiai",
        "what is gyanmasti.ai",
        "what is gyanmasti ai",
        "what is gyanmasti",
        "explain gyanmasti",
        "tell me about gyanmasti.ai",
        "tell me about gyanmasti"
    ]
    if any(q in cleaned for q in platform_questions):
        return "GYANMASTI.AI is an advanced conversational platform powered by state-of-the-art Google Gemini models, crafted to deliver a superior user experience and intelligent answers."
        
    # Predefined developer biography queries
    geetansh_questions = [
        "tell me about geetansh shukla",
        "who is geetansh shukla",
        "tell me about geetansh",
        "who is geetansh",
        "about geetansh shukla",
        "about geetansh",
        "geetansh shukla"
    ]
    if any(q in cleaned for q in geetansh_questions):
        return "Geetansh Shukla is the visionary creator, developer, and innovator behind GYANMASTI.AI, dedicated to building high-utility, beautifully designed AI systems."
        
    return None

def get_api_key():
    """Retrieve API key prioritizing Session State memory, then environmental fallback."""
    key = st.session_state.get("api_key", "").strip()
    if not key:
        key = os.environ.get("GEMINI_API_KEY", "").strip()
    return key

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None
if "api_key" not in st.session_state:
    # Set prefilled default user API Key
    st.session_state.api_key = DEFAULT_API_KEY
if "selected_theme" not in st.session_state:
    st.session_state.selected_theme = "Midnight Nebula 🌌"

# Sidebar Construction
st.sidebar.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0px;'>🤖 <span class="gradient-text">GYANMASTI</span></h1>
    <p style='text-align: center; font-size: 0.85rem; color: #94A3B8; margin-top: 0px; margin-bottom: 25px;'>
        powered by <b>Geetansh Shukla</b>
    </p>
    """,
    unsafe_allow_html=True
)

# New Chat Button (Triggered as first button in sidebar)
if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.preset_prompt = None
    st.rerun()

# 1. Chat History Section (Interactive Demo triggers)
st.sidebar.markdown(
    """
    <p style="font-size: 0.8rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 20px; margin-bottom: 8px;">
        📜 Chat History
    </p>
    """,
    unsafe_allow_html=True
)

# Render interactive buttons. If clicked, populate session state with mock conversations
for title, messages in HISTORY_DEMO.items():
    if st.sidebar.button(title, use_container_width=True):
        st.session_state.messages = messages.copy()
        st.session_state.preset_prompt = None
        st.rerun()

# 2. Creator Details Section
with st.sidebar.expander("👤 Creator Details", expanded=False):
    st.markdown(
        """
        <div style="font-size: 0.88rem; line-height: 1.6; color: #CBD5E1;">
            <b style="color:#F8FAFC; font-size:0.95rem;">Geetansh Shukla</b><br>
            <span style="color: #94A3B8; font-size: 0.78rem;">Visionary Architect & Developer</span>
            <p style="margin-top: 8px; font-size: 0.82rem; color: #94A3B8;">
                Developer specialized in crafting high-utility Generative AI systems, beautiful human-centric interfaces, and dynamic system integrations.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# 3. Contact Details Section
with st.sidebar.expander("📞 Contact Details", expanded=False):
    st.markdown(
        """
        <div style="font-size: 0.88rem; line-height: 1.6; color: #CBD5E1;">
            📧 <b>Email:</b><br>
            <a href="mailto:geetansh@gyanmasti.ai" style="color: #3B82F6; text-decoration: none;">geetansh@gyanmasti.ai</a>
            <br><br>
            🌐 <b>Website:</b><br>
            <a href="https://gyanmasti.ai" target="_blank" style="color: #A855F7; text-decoration: none;">gyanmasti.ai</a>
            <br><br>
            💼 <b>LinkedIn:</b><br>
            <a href="https://linkedin.com/in/geetansh-shukla" target="_blank" style="color: #3B82F6; text-decoration: none;">linkedin.com/in/geetansh-shukla</a>
        </div>
        """,
        unsafe_allow_html=True
    )

# 4. Theme & Aesthetics Section
with st.sidebar.expander("🎨 Theme Selection", expanded=False):
    theme_selector = st.selectbox(
        "UI Theme Gradient:",
        options=list(THEMES.keys()),
        index=list(THEMES.keys()).index(st.session_state.selected_theme)
    )
    if theme_selector != st.session_state.selected_theme:
        st.session_state.selected_theme = theme_selector
        st.rerun()

# Fetch active theme layout values
active_theme = THEMES[st.session_state.selected_theme]

# 5. Basic Settings Section
with st.sidebar.expander("⚙️ Basic Settings", expanded=False):
    # Model selector
    model_options = {
        "Gemini 1.5 Flash (Fast)": "gemini-1.5-flash",
        "Gemini 1.5 Pro (Analytical)": "gemini-1.5-pro",
    }
    selected_label = st.selectbox(
        "Model Engine:",
        options=list(model_options.keys()),
        index=0
    )
    selected_model = model_options[selected_label]
    
    # Generation settings
    temperature = st.slider(
        "Temperature (Creativity):",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Higher values make output more creative."
    )
    max_tokens = st.slider(
        "Max Output Length:",
        min_value=256,
        max_value=8192,
        value=2048,
        step=256,
        help="Maximum size of response tokens."
    )

# 6. API Key Config Section
with st.sidebar.expander("🔑 API Key Configuration", expanded=False):
    st.text_input(
        "Google Gemini API Key:",
        type="password",
        key="api_key",
        help="Google API Key used to generate model outputs."
    )

# Sidebar Footer
st.sidebar.markdown(
    """
    <div class="sidebar-footer">
        <p style="text-align: center; font-size: 0.72rem; color: #64748B; margin: 0;">
            GYANMASTI v1.2.0
        </p>
        <p style="text-align: center; font-size: 0.78rem; color: #94A3B8; margin-top: 4px; margin-bottom: 0px;">
            Powered by <b>Geetansh Shukla</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Apply dynamic CSS based on active theme
inject_custom_css(active_theme)

# Handle Preset click redirect trigger
user_input = None
if st.session_state.preset_prompt:
    user_input = st.session_state.preset_prompt
    st.session_state.preset_prompt = None

# Render Welcome Dashboard ONLY when chat history is empty
if len(st.session_state.messages) == 0:
    st.markdown(
        f"""
        <div class="welcome-container" style="max-width: 800px; margin: 40px auto 10px auto;">
            <div class="hero-banner">
                <h1 style="font-size: 3rem; margin-bottom: 10px; font-weight: 800;"><span class="gradient-text">GYANMASTI</span></h1>
                <p style="font-size: 1.25rem; color: #E2E8F0; margin-bottom: 15px;">
                    powered by <b>Geetansh Shukla</b>
                </p>
                <p style="font-size: 1rem; color: #94A3B8; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                    Experience an elite conversational platform merging advanced AI intelligence with high-fidelity glassmorphism designs, real-time theme configurations, and custom brand personalities.
                </p>
            </div>
            
            <p style="font-size: 1rem; font-weight: 600; color: #94A3B8; margin-bottom: 15px; text-align: left;">
                💡 Get Started with a Quick Action:
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # 2x2 Grid of Preset Cards
    st.markdown('<div class="welcome-container" style="max-width: 800px; margin: 0 auto;">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("💡 UI/UX Design Tips\n\nLearn how to create interfaces that wow users.", key="preset_1", use_container_width=True):
            st.session_state.preset_prompt = "What are 5 essential UI/UX design tips for making a standard app look premium and state-of-the-art?"
            st.rerun()
            
        if st.button("🤖 GenAI Use Cases\n\nDiscover cutting-edge applications for businesses.", key="preset_2", use_container_width=True):
            st.session_state.preset_prompt = "Give me 3 innovative use cases for Generative AI in business applications today."
            st.rerun()
            
    with col2:
        if st.button("🚀 Code Optimization\n\nBoost speed and performance of python code.", key="preset_3", use_container_width=True):
            st.session_state.preset_prompt = "Explain how to optimize a Python Streamlit app to render faster and handle large datasets efficiently."
            st.rerun()
            
        if st.button("🎨 Gradient Palette\n\nModern color combinations for dark theme apps.", key="preset_4", use_container_width=True):
            st.session_state.preset_prompt = "List 4 modern CSS gradient palettes for dark mode web apps, including HSL/HEX codes."
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Render Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="👤"):
            st.markdown(f'<div class="user-bubble">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(msg["content"])

# Bottom sticky chat input listener
chat_input = st.chat_input("Ask GYANMASTI anything...")
if chat_input:
    user_input = chat_input

# Process new prompt
if user_input:
    # Append user prompt to state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Render user prompt immediately
    with st.chat_message("user", avatar="👤"):
        st.markdown(f'<div class="user-bubble">{user_input}</div>', unsafe_allow_html=True)
        
    # Check for custom pre-defined creator dataset responses
    static_response = check_creator_dataset(user_input)
    
    # Render assistant response block
    with st.chat_message("assistant", avatar="🤖"):
        if static_response:
            response_placeholder = st.empty()
            full_response = ""
            # Simulate high-end typewriter animation
            for word in static_response.split():
                full_response += word + " "
                response_placeholder.markdown(full_response + "▌")
                time.sleep(0.06)
            response_placeholder.markdown(static_response)
            ai_response = static_response
        else:
            api_key = get_api_key()
            if not api_key:
                st.warning("⚠️ Google Gemini API Key is missing. Please enter your API Key in the sidebar.", icon="🔑")
                st.session_state.messages.pop() # Remove user query since response failed
                st.stop()
                
            # Display pulse loader while calling API
            loader_placeholder = st.markdown(
                """
                <div class="glowing-loader">
                    <div class="loader-dot"></div>
                    <div class="loader-dot"></div>
                    <div class="loader-dot"></div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            try:
                # Initialize GenAI Client using modern SDK
                client = genai.Client(api_key=api_key)
                
                # Configure generation parameters
                config = types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
                
                # Format conversation history using Content and Part objects
                genai_history = []
                for m in st.session_state.messages[:-1]:
                    role = "user" if m["role"] == "user" else "model"
                    genai_history.append(
                        types.Content(
                            role=role,
                            parts=[types.Part.from_text(text=m["content"])]
                        )
                    )
                
                # Initialize chat session
                chat = client.chats.create(
                    model=selected_model,
                    history=genai_history,
                    config=config
                )
                
                # Send message and get stream
                response = chat.send_message(user_input, stream=True)
                
                # Remove API call pulse loader
                loader_placeholder.empty()
                
                response_placeholder = st.empty()
                ai_response = ""
                for chunk in response:
                    ai_response += chunk.text
                    response_placeholder.markdown(ai_response + "▌")
                response_placeholder.markdown(ai_response)
                
            except Exception as e:
                # Clear loader
                loader_placeholder.empty()
                
                ai_response = f"❌ **Error generating response**: {str(e)}\n\n_Please verify your API key and internet connectivity._"
                st.error(ai_response)
                
    # Commit AI response to session state and trigger refresh
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.rerun()
