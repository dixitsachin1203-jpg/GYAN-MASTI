import streamlit as st
from google import genai
from google.genai import types

# 1. PASTE YOUR API KEY HERE
GEMINI_API_KEY = "AQ.Ab8RN6IJyltp_ScFjnb4m7PNw3vnS5XS8FQu6vKCORUz3sUQmA"

# 2. Page Configuration
st.set_page_config(
    page_title="gyanmasti.ai",
    page_icon="🧠",
    layout="centered"
)

# 3. Sidebar Configuration (Clean & Simple)
with st.sidebar:
    st.title("🚀 Status")
    st.write("Welcome to **gyanmasti.ai**!")
    st.write("Powered by **Geetansh Shukla**.")
    st.divider()
    
    # Check if key was replaced
    if GEMINI_API_KEY and GEMINI_API_KEY != "PASTE_YOUR_API_KEY_HERE":
        st.success("API Key is Configured")
    else:
        st.error("Please replace 'PASTE_YOUR_API_KEY_HERE' on line 6.")
        
    st.divider()
    st.caption("Built with Streamlit & Google GenAI SDK")

# 4. Main Interface Header
st.title("🧠 gyanmasti.ai")
st.subheader("Powered by **Geetansh Shukla**")

# 5. Chat History Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Model Logic & User Input
if prompt := st.chat_input("Ask gyanmasti.ai anything..."):
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Error validation before API call
    if not GEMINI_API_KEY or GEMINI_API_KEY == "PASTE_YOUR_API_KEY_HERE":
        with st.chat_message("assistant"):
            st.error("API Key missing! Edit line 6 in app.py to include your key.")
    else:
        try:
            # PASS KEY DIRECTLY HERE to prevent environment reading issues
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            # Request streaming response from Gemini 2.5 Flash
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                response_stream = client.models.generate_content_stream(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                # Render chunks in real-time
                for chunk in response_stream:
                    if chunk.text:
                        full_response += chunk.text
                        message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            # Save assistant response to session history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"An error occurred: {str(e)}")
