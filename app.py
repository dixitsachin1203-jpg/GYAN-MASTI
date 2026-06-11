import streamlit as st
import google.generativeai as genai
import os
import time

# Set page configuration
st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

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

def inject_custom_css():
    """Inject premium CSS styling into Streamlit to deliver an elite UI/UX experience."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Apply fonts and base dark gradient theme globally */
        html, body, [class*="css"], .stApp {
            font-family: 'Outfit', 'Inter', sans-serif !important;
            background: linear-gradient(135deg, #070913 0%, #0F172A 100%) !important;
            color: #F8FAFC !important;
        }
        
        /* Sidebar layout and border styling */
        section[data-testid="stSidebar"] {
            background-color: #06080E !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
        }
        
        section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
            padding-top: 1.5rem;
        }
        
        /* Sidebar Expander styling */
        .streamlit-expanderHeader {
            background-color: rgba(255, 255, 255, 0.02) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 10px !important;
            font-size: 0.95rem !important;
            color: #F8FAFC !important;
        }
        
        /* Text styling with Royal Blue to Purple gradient */
        .gradient-text {
            background: linear-gradient(135deg, #3B82F6 0%, #A855F7 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            letter-spacing: -0.5px;
        }
        
        /* Custom Chat bubble styles */
        div[data-testid="stChatMessage"] {
            background-color: rgba(15, 23, 42, 0.45) !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
            border-radius: 16px !important;
            padding: 16px 20px !important;
            margin-bottom: 14px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15) !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        div[data-testid="stChatMessage"]:hover {
            border-color: rgba(168, 85, 247, 0.2) !important;
            box-shadow: 0 10px 30px rgba(168, 85, 247, 0.08) !important;
            transform: translateY(-2px);
        }
        
        .user-bubble {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.08) 0%, rgba(37, 99, 235, 0.15) 100%);
            border: 1px solid rgba(59, 130, 246, 0.2) !important;
            border-radius: 14px;
            padding: 12px 16px;
            color: #F8FAFC;
            font-size: 1rem;
            line-height: 1.5;
            box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }
        
        /* Premium code formatting styling */
        code {
            background-color: rgba(255, 255, 255, 0.06) !important;
            border-radius: 6px !important;
            padding: 2px 6px !important;
            font-family: 'Courier New', Courier, monospace !important;
            color: #F472B6 !important;
        }
        pre code {
            background-color: rgba(0, 0, 0, 0.25) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            padding: 14px !important;
            border-radius: 12px !important;
            display: block !important;
            overflow-x: auto !important;
            color: #E2E8F0 !important;
        }
        
        /* New Chat Button override styling */
        div.stSidebar [data-testid="stBlock"] button {
            background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%) !important;
            border: none !important;
            border-radius: 12px !important;
            color: white !important;
            font-weight: 600 !important;
            padding: 12px 20px !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.25) !important;
        }
        
        div.stSidebar [data-testid="stBlock"] button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(124, 58, 237, 0.45) !important;
            color: white !important;
        }
        
        /* Glassmorphic Preset Prompt Cards */
        .welcome-container .stButton > button {
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
        }
        
        .welcome-container .stButton > button:hover {
            background: linear-gradient(135deg, rgba(59, 130, 246, 0.12) 0%, rgba(139, 92, 246, 0.12) 100%) !important;
            border-color: rgba(139, 92, 246, 0.3) !important;
            transform: translateY(-4px) !important;
            box-shadow: 0 10px 25px -5px rgba(139, 92, 246, 0.25) !important;
            color: #FFFFFF !important;
        }
        
        /* Chat History item boxes */
        .chat-history-container {
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .chat-history-item {
            display: flex;
            align-items: center;
            padding: 10px 14px;
            margin-bottom: 8px;
            border-radius: 10px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            font-size: 0.88rem;
            color: #CBD5E1;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .chat-history-item:hover {
            background: rgba(255, 255, 255, 0.06);
            color: #F8FAFC;
            border-color: rgba(255, 255, 255, 0.1);
        }
        .chat-icon {
            margin-right: 10px;
            font-size: 1.1rem;
        }
        
        /* Chat Input field alignment and float styling */
        div[data-testid="stChatInput"] {
            border-radius: 24px !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            background-color: rgba(10, 15, 30, 0.85) !important;
            backdrop-filter: blur(12px) !important;
            box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.3) !important;
            padding: 6px 14px !important;
        }
        
        div[data-testid="stChatInput"] textarea {
            color: #F8FAFC !important;
        }
        
        /* Hiding core Streamlit branding headers and footers */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Glowing Hero Banner */
        .hero-banner {
            background: radial-gradient(circle at top left, rgba(59, 130, 246, 0.08), transparent 45%),
                        radial-gradient(circle at bottom right, rgba(139, 92, 246, 0.08), transparent 45%);
            border: 1px solid rgba(255, 255, 255, 0.04);
            border-radius: 24px;
            padding: 40px;
            text-align: center;
            margin-bottom: 30px;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
        }
        
        /* Sidebar footer styling */
        .sidebar-footer {
            margin-top: 40px;
            padding-top: 15px;
            border-top: 1px solid rgba(255, 255, 255, 0.05);
            text-align: center;
        }
        
        /* Loading Dot Pulse Animation */
        .glowing-loader {
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 20px 0;
        }
        .loader-dot {
            width: 10px;
            height: 10px;
            margin: 0 6px;
            border-radius: 50%;
            background: linear-gradient(135deg, #3B82F6 0%, #A855F7 100%);
            animation: bounce 0.6s infinite alternate;
        }
        .loader-dot:nth-child(2) { animation-delay: 0.2s; }
        .loader-dot:nth-child(3) { animation-delay: 0.4s; }
        
        @keyframes bounce {
            to { transform: translateY(-10px); }
        }
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

# Inject styling
inject_custom_css()

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "preset_prompt" not in st.session_state:
    st.session_state.preset_prompt = None

# Sidebar Construction
st.sidebar.markdown(
    """
    <h1 style='text-align: center; margin-bottom: 0px;'>🤖 <span class="gradient-text">GYANMASTI.AI</span></h1>
    <p style='text-align: center; font-size: 0.8rem; color: #94A3B8; margin-top: 0px; margin-bottom: 25px;'>
        powered by <b>Geetansh Shukla</b>
    </p>
    """,
    unsafe_allow_html=True
)

# New Chat Button
if st.sidebar.button("➕ New Chat", use_container_width=True):
    st.session_state.messages = []
    st.session_state.preset_prompt = None
    st.rerun()

# API configuration section
with st.sidebar.expander("🔑 API Key Configuration", expanded=False):
    env_key = os.environ.get("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Google Gemini API Key:",
        value=st.session_state.get("api_key", env_key),
        type="password",
        help="Input your Gemini API Key here. Stored locally in RAM only."
    )
    if api_key_input:
        st.session_state.api_key = api_key_input

# Model configuration settings
with st.sidebar.expander("⚙️ Model Settings", expanded=False):
    model_options = {
        "Gemini 1.5 Flash (Fast)": "gemini-1.5-flash",
        "Gemini 1.5 Pro (Analytical)": "gemini-1.5-pro",
    }
    selected_label = st.selectbox(
        "Select Model Version:",
        options=list(model_options.keys()),
        index=0
    )
    st.session_state.selected_model = model_options[selected_label]

# Demo Chat History list
st.sidebar.markdown(
    """
    <div class="chat-history-container">
        <p style="font-size: 0.85rem; font-weight: 600; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 10px;">
            Recent Chats (Demo)
        </p>
        <div class="chat-history-item"><span class="chat-icon">⚡</span> UI/UX Optimization Checklist</div>
        <div class="chat-history-item"><span class="chat-icon">🎨</span> Premium Glassmorphism Guide</div>
        <div class="chat-history-item"><span class="chat-icon">🤖</span> Gemini Integration Sandbox</div>
        <div class="chat-history-item"><span class="chat-icon">🔮</span> Advanced Python Tips</div>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar Footer
st.sidebar.markdown(
    """
    <div class="sidebar-footer">
        <p style="text-align: center; font-size: 0.75rem; color: #64748B; margin: 0;">
            GYANMASTI.AI v1.0.0
        </p>
        <p style="text-align: center; font-size: 0.8rem; color: #94A3B8; margin-top: 4px; margin-bottom: 0px;">
            Powered by <b>Geetansh Shukla</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Handle Preset click redirect trigger
user_input = None
if st.session_state.preset_prompt:
    user_input = st.session_state.preset_prompt
    st.session_state.preset_prompt = None

# Render Welcome Dashboard ONLY when chat history is empty
if len(st.session_state.messages) == 0:
    st.markdown(
        """
        <div class="welcome-container" style="max-width: 800px; margin: 40px auto 10px auto;">
            <div class="hero-banner">
                <h1 style="font-size: 3rem; margin-bottom: 10px; font-weight: 800;"><span class="gradient-text">GYANMASTI.AI</span></h1>
                <p style="font-size: 1.25rem; color: #E2E8F0; margin-bottom: 15px;">
                    powered by <b>Geetansh Shukla</b>
                </p>
                <p style="font-size: 1rem; color: #94A3B8; max-width: 600px; margin: 0 auto; line-height: 1.6;">
                    Experience a elite conversational platform that merges advanced AI intelligence with high-fidelity glassmorphism designs, fluid animations, and custom model personalities.
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
chat_input = st.chat_input("Ask GYANMASTI.AI anything...")
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
                # Configure API key
                genai.configure(api_key=api_key)
                
                # Fetch target model version
                model_name = st.session_state.get("selected_model", "gemini-1.5-flash")
                
                model = genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=SYSTEM_INSTRUCTION
                )
                
                # Format conversation history
                chat_context = []
                for m in st.session_state.messages[:-1]:
                    chat_context.append({
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [m["content"]]
                    })
                
                # Initialize chat and send query
                chat = model.start_chat(history=chat_context)
                
                # Stream responses
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
