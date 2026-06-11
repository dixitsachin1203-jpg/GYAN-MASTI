import streamlit as st
import os
from openai import OpenAI

# -----------------------------------------------------------------------------
# 1. APPLICATION VIEWPORT AND PAGE LAYOUT CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="GyanMasti.ai",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Cyber-Neon Ambient Interface Custom CSS
custom_theme_css = """
<style>
    /* Absolute Base Background Reset */
    .stApp {
        background: linear-gradient(135deg, #0d0a1b 0%, #130f26 50%, #050408 100%) !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    /* Interactive Moving Header Title */
    .brand-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(45deg, #00f2fe, #4facfe, #9b51e0, #ff007f);
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

    /* Glassmorphic Cyber Workspace Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(12, 8, 24, 0.75) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(0, 242, 254, 0.2) !important;
    }

    /* Custom Layout Architecture For Conversational Rows */
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

    /* Ergonomic Speech Bubbles */
    .message-bubble {
        padding: 1.2rem 1.6rem;
        border-radius: 22px;
        max-width: 78%;
        line-height: 1.6;
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        font-size: 1.05rem;
    }
    
    /* User: Hot Pink Radical Gradient Bubble */
    .user .message-bubble {
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%);
        color: #ffffff !important;
        border-bottom-right-radius: 2px;
        border: 1px solid rgba(255, 255, 255, 0.15);
    }

    /* Assistant: Translucent Cyber Blue Shield Bubble */
    .assistant .message-bubble {
        background: rgba(22, 17, 45, 0.65);
        color: #f1f5f9 !important;
        border-bottom-left-radius: 2px;
        border: 1px solid rgba(0, 242, 254, 0.25);
        backdrop-filter: blur(10px);
    }
    
    /* Global Footer Accent Styling */
    .footer-text {
        text-align: center;
        color: #5d5d75;
        font-size: 0.85rem;
        margin-top: 4rem;
        border-top: 1px solid rgba(255, 255, 255, 0.06);
        padding-top: 1.2rem;
    }
    
    /* Input Field Overrides */
    div[data-testid="stChatInput"] textarea {
        background-color: rgba(18, 13, 33, 0.85) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 242, 254, 0.35) !important;
        border-radius: 14px !important;
    }
</style>
"""
st.markdown(custom_theme_css, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. CONTROL COMPONENT SIDEBAR & INITIAL VALUE LOADERS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe; margin-top:0;'>⚙️ Matrix Core Controls</h2>", unsafe_allow_html=True)
    st.write("Engine system metrics operating on ultra-low latency **Groq Infrastructure**.")
    
    # Priority verification flow for checking secure variable storage paths
    saved_key = ""
    if "GROQ_API_KEY" in st.secrets:
        saved_key = st.secrets["GROQ_API_KEY"]
    elif os.environ.get("GROQ_API_KEY"):
        saved_key = os.environ.get("GROQ_API_KEY")
        
    user_api_key = st.text_input(
        "Groq Cloud API Key",
        value=saved_key,
        type="password",
        placeholder="gsk_...",
        help="Acquire a free generation token value instantly by entering ://groq.com"
    )
    
    st.markdown("---")
    st.markdown("<h3 style='color:#ff007f;'>🤖 Parameter Controls</h3>", unsafe_allow_html=True)
    
    # Selection module for fast inference systems available on Groq platforms
    selected_model = st.selectbox(
        "AI Brain Engine",
        [
            "llama-3.3-70b-versatile", 
            "llama3-8b-8192", 
            "gemma2-9b-it"
        ],
        index=0,
        help="Llama-3.3-70b delivers maximum accuracy and advanced reasoning depth."
    )
    
    creativity_index = st.slider("Temperature Configuration", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
    
    # Context Reset Button Implementation
    if st.button("🧹 Flush Memory Banks", use_container_width=True):
        st.session_state.messages = [
            {"role": "assistant", "content": "Memory wipe completed. Systems normal. What instruction set shall we process next, boss?"}
        ]
        st.rerun()
    
    # Custom Personality Prompt Directives defining GyanMasti.ai limits
    system_instruction_prompt = (
        "You are GyanMasti.ai, an elite, highly intelligent, and universally capable AI model. "
        "You are proudly designed, developed, and powered by your creator, Geetansh Shukla. "
        "Maintain an engaging, brilliantly smart, helpful, witty, and high-energy tone. "
        "Always proudly acknowledge that your creator is Geetansh Shukla whenever contextually relevant."
    )
    
    st.markdown("---")
    st.markdown(
        "<div style='color: #6a6a85; font-size:0.8rem; text-align:center;'>"
        "GyanMasti.ai Core • Release v3.5<br>© 2026 Geetansh Shukla"
        "</div>", 
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 3. INTERFACE FRAMEWORK DISPLAY AND INITIALIZATION 
# -----------------------------------------------------------------------------
st.markdown("<h1 class='brand-title'>GyanMasti.ai</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>⚡ Powered by Geetansh Shukla</p>", unsafe_allow_html=True)

# Instantiate memory tracking elements within local state dictionaries
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Salutations. I am GyanMasti.ai, engineered by Geetansh Shukla. Powered by high-speed Groq processing clusters. Let's build something incredible."}
    ]

# Render operational history tracking layout
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for current_msg in st.session_state.messages:
    if current_msg["role"] != "system":
        message_origin_class = "user" if current_msg["role"] == "user" else "assistant"
        st.markdown(
            f'<div class="message-row {message_origin_class}">'
            f'<div class="message-bubble">{current_msg["content"]}</div>'
            f'</div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. CHAT PROCESSING WORKFLOW AND TOKENS STREAMING
# -----------------------------------------------------------------------------
if client_query := st.chat_input("Inquire anything from GyanMasti.ai..."):
    
    # Instantly project user question block onto frontend screen
    st.markdown(
        f'<div class="message-row user">'
        f'<div class="message-bubble">{client_query}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.session_state.messages.append({"role": "user", "content": client_query})
    
    # Terminate request execution safely if no valid auth configuration token is found
    if not user_api_key:
        st.error("⚠️ Authentication Missing: Please provide a valid Groq Cloud API Key (`gsk_...`) inside the Matrix Controls sidebar panel.")
    else:
        try:
            # Connect pipeline utilizing standard Groq Cloud base target addresses
            api_client = OpenAI(
                api_key=user_api_key,
                base_url="https://groq.com"
            )
            
            # Pack memory timeline records together with system behavior scripts
            runtime_payload = [{"role": "system", "content": system_instruction_prompt}]
            for history_item in st.session_state.messages:
                runtime_payload.append({"role": history_item["role"], "content": history_item["content"]})
                
            with st.spinner("⚡ Processing Neural Request Stream..."):
                response_stream_object = api_client.chat.completions.create(
                    model=selected_model,
                    messages=runtime_payload,
                    temperature=creativity_index,
                    stream=True
                )
                
                realtime_text_accumulator = ""
                screen_placeholder_slot = st.empty()
                
                # Capture and print incoming generation text packets sequentially
                for network_chunk in response_stream_object:
                    if network_chunk.choices[0].delta.content:
                        realtime_text_accumulator += network_chunk.choices[0].delta.content
                        screen_placeholder_slot.markdown(
                            f'<div class="message-row assistant">'
