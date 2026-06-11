import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. INSERT YOUR GEMINI API KEY HERE
# ==========================================
GEMINI_API_KEY = AQ.Ab8RN6JHzZL_xKV_RdnMufeK5uGtm3vZ-sbRpv7mgAbH-87E_Q

# --- PAGE SETUP & UI CONFIGURATION ---
st.set_page_config(
    page_title="Gemini AI Chatbot", 
    page_icon="🤖", 
    layout="centered"
)

st.title("🤖 Gemini AI Chatbot")
st.caption("A dedicated private chat workspace powered by Google Gemini.")

# --- SIDEBAR TOOLS ---
with st.sidebar:
    st.header("Workspace Tools")
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- INITIALIZE API & MODEL ---
# Validate that the placeholder text has been swapped out
if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE" or not GEMINI_API_KEY:
    st.error("⚠️ Setup Missing: Please replace 'YOUR_GEMINI_API_KEY_HERE' in the python script with your real Gemini API key.")
    st.stop()

# Configure the official SDK directly with your embedded key
genai.configure(api_key=GEMINI_API_KEY)

try:
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction="You are a helpful, brilliant, and polite AI assistant modeled after ChatGPT and Gemini. Give concise, well-formatted answers."
    )
except Exception as e:
    st.error(f"Failed to initialize the Gemini model: {str(e)}")
    st.stop()

# --- SESSION STATE CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous chat blocks on screen refreshment
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- EXECUTE ACTIVE CHAT LOOP ---
if prompt := st.chat_input("Ask me anything..."):
    
    # 1. Print user message on the interface screen
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 2. Append to continuous background memory state
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Format total active dialog stream for Gemini context ingestion 
    api_history = []
    for msg in st.session_state.messages:
        api_role = "user" if msg["role"] == "user" else "model"
        api_history.append({
            "role": api_role, 
            "parts": [msg["content"]]
        })

    # 4. Stream conversational response chunk-by-chunk
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        try:
            response = model.generate_content(api_history, stream=True)
            
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    # Display a blinking loading cursor block
                    response_placeholder.markdown(full_response + "▌")
            
            # Print final clean message block 
            response_placeholder.markdown(full_response)
            
            # 5. Lock bot reply string into memory state
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"API Connection Error: {str(e)}")
