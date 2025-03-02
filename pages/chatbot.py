import streamlit as st
from openai import OpenAI

st.title("Awesome Chatbot")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Say something")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            stream=True
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
