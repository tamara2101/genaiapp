# STREAMLIT APP WITH STREAMING

import streamlit as st
import hmac
import uuid
import time
import os
from openai import OpenAI
from assistant import gpts
from dotenv import load_dotenv, find_dotenv
from openai.types.beta.assistant_stream_event import ThreadMessageDelta
from openai.types.beta.threads.text_delta_block import TextDeltaBlock

# Load environment variables
_ = load_dotenv(find_dotenv())

# Initialize OpenAI client
client = OpenAI()

#--------------------------------------------
# LOGIN
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("AI Tutor", key="gpt")
            st.text_input("Passwort", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["gpt"] in st.secrets["passwords"] and hmac.compare_digest(
                st.session_state["password"],
                st.secrets.passwords[st.session_state["gpt"]],
        ):
            st.session_state["password_correct"] = True
            st.session_state["logged_in_user"] = st.session_state["gpt"]  
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 AI Tutor nicht bekannt oder Passwort falsch")
    return False

if not check_password():
    st.stop()

if "logged_in_user" in st.session_state:
    custom_gpt = st.session_state["logged_in_user"]

#-------------------------------------------
# SELECT CUSTOM GPT
custom_gpt = st.session_state["logged_in_user"]
assistant_id = gpts[custom_gpt]

#--------------------------------------------
# Initialize session state variables
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "run" not in st.session_state:
    st.session_state.run = {"status": None}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "retry_error" not in st.session_state:
    st.session_state.retry_error = 0

#--------------------------------------------
# APP STARTS HERE
st.set_page_config(page_title="AI Tutor")

# Sidebar
st.sidebar.title("AI Tutor")
st.sidebar.write(custom_gpt)
st.sidebar.write("*Bitte eine Frage in das Chatfenster eingeben*")
st.sidebar.divider()

#Initialize OpenAI
if "assistant" not in st.session_state:
    st.session_state.assistant = client.beta.assistants.retrieve(assistant_id)
    st.session_state.thread = client.beta.threads.create(
        metadata={'session_id': st.session_state.session_id}
    )

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input and message creation
if prompt := st.chat_input("Wie kann ich weiterhelfen?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=prompt
    )

    # Run the assistant with streaming
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        stream = client.beta.threads.runs.create(
            thread_id=st.session_state.thread.id,
            assistant_id=st.session_state.assistant.id,
            stream=True
        )
        
        for event in stream:
            if isinstance(event, ThreadMessageDelta):
                if isinstance(event.data.delta.content[0], TextDeltaBlock):
                    full_response += event.data.delta.content[0].text.value
                    message_placeholder.markdown(full_response + "▌")
        
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Handle run status (this part may not be necessary with streaming, but kept for consistency)
if hasattr(st.session_state.run, 'status'):
    if st.session_state.run.status == "failed":
        st.error("Fehler: Die OpenAI-API verarbeitet derzeit zu viele Anfragen. Bitte versuchen Sie es später erneut.")