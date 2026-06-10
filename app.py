import streamlit as st
import time
import random

# 1. Page Configuration
st.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# 2. Sidebar / Dashboard Controls
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    st.markdown("Adjust settings to test interface behavior.")
    
    # AI Personality Selector
    ai_tone = st.selectbox(
        "AI Personality Mode",
        ["Standard Tech", "Sarcastic Genius", "Ultra Professional", "Motivational Coach"]
    )
    
    # Creativity slider mock
    st.slider("Creativity (Temperature)", 0.0, 1.0, 0.7)
    
    # System Status Indicator
    st.markdown("---")
    st.markdown("### 🖥️ Engine Status")
    st.success("UI Interface: Active")
    st.warning("API Engine: Demo Mode (Offline)")
    
    # Clear Chat Button
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# 3. Main App Header & Branding
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🧠 GYANMASTI.AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888888; font-size: 1.1rem; margin-top: 0;'>Powered by Geetansh Shukla</p>", unsafe_allow_html=True)
st.markdown("---")

# 4. Initialize Demo Data & Message States
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to **GYANMASTI.AI**! 👋 I am currently running in **Demo UI Mode** (no API required). Ask me anything to test out my slick streaming chat animation!"}
    ]

# Mock Responses Database based on Tone selection
MOCK_RESPONSES = {
    "Standard Tech": [
        "That is a fascinating concept. From a technological standpoint, implementing this would require robust system architecture.",
        "Processing request... parsed text successfully. The theoretical outcome looks highly optimal.",
        "Interesting question! If we hook up the live API later, I will give you real-time data on that exact topic."
    ],
    "Sarcastic Genius": [
        "Oh, wow. What an absolute groundbreaking question. Let me strain my simulated circuits to answer that.",
        "I could give you a brilliant answer, but I am currently running on a fake offline brain. Try again later!",
        "Error 404: True intelligence not found. (Just kidding, the UI works perfectly, but my API is still asleep)."
    ],
    "Ultra Professional": [
        "Thank you for your inquiry. This specific matter warrants a detailed analytical review once backend integrations are completed.",
        "An excellent proposition. We look forward to executing this request with absolute precision in production.",
        "Please note that under current demo parameters, historical data points are simulated for presentation purposes."
    ],
    "Motivational Coach": [
        "Boom! What an incredible question! You are pushing the boundaries of what **GYANMASTI.AI** can achieve!",
        "Remember, every great application starts with a beautiful interface just like this one. Keep building!",
        "That is the spirit! Geetansh Shukla built this beautiful framework, and you are ready to conquer the next step!"
    ]
}

# 5. Render Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input Logic
if user_query := st.chat_input("Ask GYANMASTI.AI anything..."):
    
    # Render user query instantly
    with st.chat_message("user"):
        st.markdown(user_query)
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Render simulated assistant reply
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # Pick a random response matching the selected personality
        raw_response = random.choice(MOCK_RESPONSES[ai_tone])
        full_response = f"**[Demo Mode - {ai_tone}]**\n\n{raw_response}"
        
        # Simulate typing/streaming effect word by word
        displayed_text = ""
        for word in full_response.split(" "):
            displayed_text += word + " "
            time.sleep(0.06)  # Speeds up/slows down typing effect
            response_placeholder.markdown(displayed_text + "▌")
            
        # Remove typing cursor when done
        response_placeholder.markdown(displayed_text)
        
    # Save assistant message to session memory
    st.session_state.messages.append({"role": "assistant", "content": displayed_text})
