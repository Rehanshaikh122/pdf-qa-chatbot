import streamlit as st
import requests

st.set_page_config(page_title="PDF Q&A Bot", page_icon="💬")

st.markdown(
    """
    <style>
    .chat-bubble-user {
        background-color: #DCF8C6;
        color: black;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px;
        max-width: 70%;
        float: right;
        clear: both;
    }
    .chat-bubble-bot {
        background-color: #ECECEC;
        color: black;
        padding: 10px 15px;
        border-radius: 15px;
        margin: 5px;
        max-width: 70%;
        float: left;
        clear: both;
    }
    .chat-container {
        display: flex;
        flex-direction: column;
    }
    .source-text {
        font-size: 0.8em;
        color: #555;
        margin-left: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💬 PDF Q&A Chatbot")
st.write("Ask me anything from the manual!")

API_URL = "http://localhost:8000/ask"

if "history" not in st.session_state:
    st.session_state.history = []

# Input field
user_query = st.text_input("💬 Type your question here:")

if st.button("Send") and user_query.strip() != "":
    try:
        response = requests.post(API_URL, json={"query": user_query})
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "No answer found")
            sources = data.get("sources", [])

            st.session_state.history.append(("user", user_query, []))
            st.session_state.history.append(("bot", answer, sources))
        else:
            st.error("❌ Backend error. Make sure FastAPI server is running.")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")

# Chat display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for sender, msg, src in st.session_state.history:
    if sender == "user":
        st.markdown(f"<div class='chat-bubble-user'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-bot'>{msg}</div>", unsafe_allow_html=True)
        if src:
            st.markdown(f"<div class='source-text'>📄 Sources: {', '.join(src)}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
