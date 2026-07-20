"""
-------------------------------------------------------

File: chat_history.py

Purpose:
Manage Streamlit chat history and provide
conversation context for GPT.

-------------------------------------------------------
"""

from datetime import datetime
import streamlit as st


# ----------------------------------------------------
# Initialize Chat
# ----------------------------------------------------

def initialize_chat():
    """
    Initialize chat history.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []


# ----------------------------------------------------
# Add Message
# ----------------------------------------------------

def add_message(role: str, content: str):
    """
    Add a message to chat history.

    Parameters
    ----------
    role : str
        user / assistant

    content : str
    """

    st.session_state.messages.append(
        {
            "role": role,
            "content": content,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    )


# ----------------------------------------------------
# Display Chat
# ----------------------------------------------------

def display_chat():
    """
    Display chat history.
    """

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


# ----------------------------------------------------
# Get Messages
# ----------------------------------------------------

def get_messages():
    """
    Return all chat messages.
    """

    return st.session_state.messages


# ----------------------------------------------------
# Last User Message
# ----------------------------------------------------

def get_last_user_message():

    for message in reversed(st.session_state.messages):

        if message["role"] == "user":

            return message["content"]

    return None


# ----------------------------------------------------
# Last Assistant Message
# ----------------------------------------------------

def get_last_assistant_message():

    for message in reversed(st.session_state.messages):

        if message["role"] == "assistant":

            return message["content"]

    return None


# ----------------------------------------------------
# GPT Conversation Context
# ----------------------------------------------------

def get_chat_context(max_messages: int = 6):
    """
    Return the latest conversation in GPT format.

    Example

    [
        {"role":"user","content":"..."},
        {"role":"assistant","content":"..."}
    ]
    """

    history = st.session_state.messages[-max_messages:]

    context = []

    for message in history:

        context.append(

            {
                "role": message["role"],
                "content": message["content"]
            }

        )

    return context


# ----------------------------------------------------
# Conversation Summary
# ----------------------------------------------------

def export_chat():

    conversation = []

    for message in st.session_state.messages:

        role = message["role"].capitalize()

        time = message["timestamp"]

        conversation.append(

            f"[{time}] {role}: {message['content']}"

        )

    return "\n\n".join(conversation)


# ----------------------------------------------------
# Chat Statistics
# ----------------------------------------------------

def chat_statistics():

    total = len(st.session_state.messages)

    users = len(

        [

            m

            for m in st.session_state.messages

            if m["role"] == "user"

        ]

    )

    assistants = len(

        [

            m

            for m in st.session_state.messages

            if m["role"] == "assistant"

        ]

    )

    return {

        "total_messages": total,

        "user_messages": users,

        "assistant_messages": assistants

    }


# ----------------------------------------------------
# Clear Chat
# ----------------------------------------------------

def clear_chat():

    st.session_state.messages = []


# ----------------------------------------------------
# Download Chat
# ----------------------------------------------------

def download_chat():

    return export_chat()