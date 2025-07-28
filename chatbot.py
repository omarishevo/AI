# chatbot_app.py

import openai
import streamlit as st

# UI title
st.set_page_config(page_title="🤖 AI Chatbot", layout="centered")
st.title("🤖 AI Chatbot using OpenAI API")

# Input your OpenAI API key here or use a config file/environment variable
openai.api_key = st.secrets["OPENAI_API_KEY"] if "OPENAI_API_KEY" in st.secrets else st.text_input("Enter your OpenAI API Key:", type="password")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]

# User input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Display user message
    st.chat_message("user").write(user_input)

    # Append to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Call OpenAI API
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if you have access
            messages=st.session_state.messages
        )
        reply = response.choices[0].message["content"]
        st.chat_message("assistant").write(reply)

        # Append reply to history
        st.session_state.messages.append({"role": "assistant", "content": reply})

    except Exception as e:
        st.error(f"Error: {e}")
