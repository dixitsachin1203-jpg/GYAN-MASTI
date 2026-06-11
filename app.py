import streamlit as st
import os
from google import genai
from google.genai import types

# 1. PAGE SETTINGS & PREMIUM THEME
st.set_page_config(
    page_title="GyanMasti.ai",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

custom_css = """
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c1b 0%, #15102a 50%, #060409 100%);
        color: #e0e0ff;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
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
    section[data-testid="stSidebar"] {
        background: rgba(15, 10, 30, 0.7) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 0, 127, 0.2);
    }
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
    .user .message-bubble {
        background: linear-gradient(135deg, #ff007f 0%, #7928ca 100%);
        color: #ffffff;
        border-bottom-right-radius: 2px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .assistant .message-bubble {
        background: rgba(25, 20, 50, 0.6);
        color: #e2e8f0;
        border-bottom-left-radius: 2px;
        border: 1px solid rgba(0, 242, 254, 0.3);
        backdrop-filter: blur(8px);
    }
    .footer-text {
        text-align: center;
        color: #6b6b83;
        font-size: 0.85rem;
        margin-top: 3rem;
        border-top: 1px solid rgba(255,255,255,0.05);
        padding-top: 1rem;
    }
    div[data-testid="stChatInput"] textarea {
        background-color: rgba(20, 15, 35, 0.8) !important;
        color: #ffffff !important;
        border: 1px solid rgba(0, 242, 254, 0.4) !important;
        border-radius: 12px !important;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# 2. KEY LOGIC & CONTROLS
with st.sidebar:
    st.markdown("<h2 style='color:#00f2fe; margin-top:0;'>⚙️ Matrix Control</h2>", unsafe_allow_html=True)
    
    default_key = ""
    if "GEMINI_API_KEY" in st.secrets:
        default_key = st.secrets["GEMINI_API_KEY"]
    elif os.environ.get("GEMINI_API_KEY"):
        default_key = os.environ.get("GEMINI_API_KEY")
        
    api_key_input = st.text_input(
        "Google Gemini API Key",
        value=default_key,
        type="password",
        placeholder="AIzaSy..."
    )
    
    st.markdown("---")
    model_choice = st.selectbox("Select Model Variant", ["gemini-2.5-flash", "gemini-2.5-pro"])
    creativity = st.slider("Creativity (Temperature)", min_value=0.0, max_value=2.0, value=0.7)
    
    system_instruction = (
        "You are GyanMasti.ai, an elite, highly intelligent, and universally capable AI model. "
        "You are proudly designed and powered by your creator, Geetansh Shukla. "
        "Maintain an engaging, brilliantly smart, helpful, and energetic tone."
    )

# 3. INTERFACE HEADER & HISTORY
st.markdown("<h1 class='brand-title'>GyanMasti.ai</h1>", unsafe_allow_html=True)
st.markdown("<p class='brand-subtitle'>⚡ Powered by Geetansh Shukla</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome. I am GyanMasti.ai, engineered by Geetansh Shukla. How can I assist you today?"}
    ]

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

# 4. CHAT LOGIC WITH INLINE STREAM CORRECTION
if user_query := st.chat_input("Inquire anything from GyanMasti.ai..."):
    st.markdown(
        f'<div class="message-row user">'
        f'<div class="message-bubble">{user_query}</div>'
        f'</div>',
        unsafe_allow_html=True
    )
    st.session_state.messages.append({"role": "user", "content": user_query})
    
    if not api_key_input:
        st.error("⚠️ Security Authentication Missing: Please provide your key in the sidebar.")
    else:
        try:
            client = genai.Client(api_key=api_key_input)
            formatted_contents = []
            for m in st.session_state.messages:
                api_role = "user" if m["role"] == "user" else "model"
                formatted_contents.append(
                    types.Content(role=api_role, parts=[types.Part.from_text(text=m["content"])])
                )
            
            with st.spinner("⚡ Processing..."):
                response_stream = client.models.generate_content_stream(
                    model=model_choice,
                    contents=formatted_contents,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=creativity,
                    ),
                )
                
                assistant_response = ""
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
                
                response_placeholder.markdown(
                    f'<div class="message-row assistant">'
                    f'<div class="message-bubble">{assistant_response}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
                
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
        except Exception as e:
            st.error(f"❌ Connection Error: {str(e)}")

st.markdown("<div class='footer-text'>GyanMasti.ai Framework • Lovingly Crafted by Geetansh Shukla</div>", unsafe_allow_html=True)
