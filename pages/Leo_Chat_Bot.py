import streamlit as st
from openai import OpenAI

st.title("Ask Leo!")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# --- SIDEBAR NAVIGATION ---
# st.sidebar.title("Navigation")
# st.sidebar.page_link("Home.py", label="🏠 Home")
# st.sidebar.page_link("pages/About_Leo.py", label="ℹ️ About Leo")
# st.sidebar.page_link("pages/My_Recipe.py", label="📊 My Recipes")
# st.sidebar.page_link("pages/Leo_Chat_Bot.py", label="🤖 Chat Bot")
# st.sidebar.page_link("pages/Share_Your_Meal.py", label="📝 Share Your Meal")
# st.sidebar.page_link("pages/My_Profile.py", label="👤 My Profile")
# st.sidebar.page_link("pages/Authentication.py", label="🔑 Login/Register")


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
