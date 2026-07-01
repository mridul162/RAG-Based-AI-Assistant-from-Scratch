"""
streamlit_app.py

Simple Streamlit frontend for the
RAG-Based-AI-Assistant project.
"""

import requests
import streamlit as st
import uuid


if "phone_number" not in st.session_state:
    st.session_state.phone_number = str(uuid.uuid4())

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------

API_URL = "https://ecommerce-ai-assistant-rvqu.onrender.com/chat"

# Example for deployed backend:
# API_URL = "https://your-render-app.onrender.com/chat"


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="Hasanah Mart AI Assistant",
    page_icon="🤖",
    layout="wide"
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🤖 Hasanah Mart AI Assistant")

st.caption(
    "Multilingual RAG-Based AI Assistant "
    "(Bangla • English • Banglish)"
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------------------------------------------------------
# DISPLAY CHAT HISTORY
# ---------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# USER INPUT
# ---------------------------------------------------------

query = st.chat_input(
    "Ask a question..."
)


# ---------------------------------------------------------
# PROCESS QUERY
# ---------------------------------------------------------

if query:

    # ---------------------------------------------
    # Display User Message
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):

        st.markdown(query)

    # ---------------------------------------------
    # Call Backend
    # ---------------------------------------------

    try:

        with st.spinner(
            "Thinking..."
        ):

            response = requests.post(
                API_URL,
                json={
                    "phone_number": st.session_state.phone_number,
                    "message": query
                },
                timeout=60
            )

            response.raise_for_status()

            data = response.json()

            answer = data.get(
                "answer",
                "No answer returned."
            )

    except Exception as e:

        answer = (
            f"❌ Error contacting backend:\n\n{e}"
        )

    # ---------------------------------------------
    # Display Assistant Response
    # ---------------------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message(
        "assistant"
    ):

        st.markdown(answer)