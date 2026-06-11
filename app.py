import streamlit as tf
from google import genai
from google.genai import types
import os

# Paste your actual Google Gemini API key inside the quotes below:
GEMINI_API_KEY = "AQ.Ab8RN6IJyltp_ScFjnb4m7PNw3vnS5XS8FQu6vKCORUz3sUQmA"

# Automatically inject the key into the system environment memory
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# 1. Page Configuration
tf.set_page_config(
    page_title="gyanmasti.ai",
    page_icon="🧠",
    layout="centered"
)

# 2. Sidebar Configuration (Clean & Simple)
with tf.sidebar:
    tf.title("🚀 Status")
    tf.write("Welcome to **gyanmasti.ai**!")
    tf.write("Powered by **Geetansh Shukla**.")
    tf.divider()
    
    # Verify the code has your key
    if GEMINI_API_KEY and GEMINI_API_KEY != "PASTE_YOUR_API_KEY_HERE":
        tf.success("Connected to Gemini API")
    else:
        tf.error("Please replace 'PASTE_YOUR_API_KEY_HERE' with your real key.")
        
    tf.divider()
    tf.caption("Built with Streamlit & Google GenAI SDK")

# 3. Main Interface Header
tf.title("🧠 gyanmasti.ai")
tf.subheader("Powered by **Geetansh Shukla**")

# 4. Chat History Initialization
if "messages" not in tf.session_state:
    tf.session_state.messages = []

# Display previous chat messages
for message in tf.session_state.messages:
    with tf.chat_message(message["role"]):
        tf.markdown(message["content"])

# 5. Model Logic & User Input
if prompt := tf.chat_input("Ask gyanmasti.ai anything..."):
    
    # Display user message immediately
    with tf.chat_message("user"):
        tf.markdown(prompt)
    tf.session_state.messages.append({"role": "user", "content": prompt})

    # Error handling if key is missing
    if not GEMINI_API_KEY or GEMINI_API_KEY == "PASTE_YOUR_API_KEY_HERE":
        with tf.chat_message("assistant"):
            tf.error("API Key missing! Edit line 6 in app.py to include your key.")
    else:
        try:
            # Initialize client (picks up key from os.environ automatically)
            client = genai.Client()
            
            # Request streaming response from Gemini 2.5 Flash
            with tf.chat_message("assistant"):
                message_placeholder = tf.empty()
                full_response = ""
                
                response_stream = client.models.generate_content_stream(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                # Render chunks in real-time
                for chunk in response_stream:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
                
                message_placeholder.markdown(full_response)
            
            # Save assistant response to session history
            tf.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            with tf.chat_message("assistant"):
                tf.error(f"An error occurred: {str(e)}")
