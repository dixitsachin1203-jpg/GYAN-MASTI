import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬", layout="centered")
st.title("💬 Gemini AI Chatbot")
st.caption("A simple GPT/Gemini clone powered by Google Gemini API")

# --- API KEY AUTHENTICATION ---
# Users can securely input their API key via the sidebar
with st.sidebar:
    api_key_input = st.text_input("AQ.Ab8RN6JHzZL_xKV_RdnMufeK5uGtm3vZ-sbRpv7mgAbH-87E_Q:", type="password")
    st.markdown("[Get a free Gemini API Key](
