import streamlit as bae
import g4f

# Configure page settings
bae.set_page_config(
    page_title="GYANMASTI.AI",
    page_icon="🧠",
    layout="centered"
)

# App Branding Header
bae.title("🧠 GYANMASTI.AI")
bae.caption("🚀 Powered by Geetansh Shukla")
bae.markdown("---")

# Initialize chat history session state
if "messages" not in bae.session_state:
    bae.session_state.messages = []

# Display existing chat history
for message in bae.session_state.messages:
    with bae.chat_message(message["role"]):
        bae.markdown(message["content"])

# Accept user input
if user_query := bae.chat_input("Ask GYANMASTI.AI anything..."):
    
    # Display user message
    bae.chat_message("user").markdown(user_query)
    bae.session_state.messages.append({"role": "user", "content": user_query})

    # Generate response from the AI model
    with bae.chat_message("assistant"):
        response_placeholder = bae.empty()
        
        try:
            # Call the free interference model provider
            response = g4f.ChatCompletion.create(
                model=g4f.models.gpt_4,
                messages=bae.session_state.messages,
            )
            
            # Display response and save to history
            response_placeholder.markdown(response)
            bae.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            response_placeholder.error("Oops! Something went wrong. Please try again.")
