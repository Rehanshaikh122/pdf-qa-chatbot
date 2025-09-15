import streamlit as st
import requests

st.set_page_config(page_title="PDF Q&A Chatbot", page_icon="🤖", layout="centered")

# Custom CSS for colorful chat bubbles
st.markdown(
    """
    <style>
    .chat-container {
        max-width: 700px;
        margin: auto;
        padding: 10px;
    }
    .user-msg {
        background-color: #4F9DFF;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0px 15px;
        margin: 8px 0;
        text-align: right;
    }
    .bot-msg {
        background-color: #EDEDED;
        color: black;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0px;
        margin: 8px 0;
        text-align: left;
    }
    .title {
        text-align: center;
        font-size: 30px;
        font-weight: bold;
        margin-bottom: 20px;
        color: #333333;
    }
    .subtitle {
        text-align: center;
        font-size: 16px;
        margin-bottom: 30px;
        color: #555555;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown('<div class="title">🤖 PDF Q&A Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask questions from your PDF and chat continuously!</div>', unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input form at bottom
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Type your question:", "", placeholder="Ask something from the PDF...")
    submitted = st.form_submit_button("Send")

if submitted and user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        response = requests.post("http://localhost:8000/ask", json={"question": user_input})
        bot_reply = response.json().get("answer", "❌ Sorry, I couldn’t find an answer.")
    except:
        bot_reply = "⚠️ Backend server not running. Please start `server.py`."

    # Add bot reply
    st.session_state.messages.append({"role": "bot", "content": bot_reply})

    # Rerun app
    st.rerun()
