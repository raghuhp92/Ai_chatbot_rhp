# import truststore
# truststore.inject_into_ssl()

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

st.set_page_config(
    page_title="chat-RHP",
    page_icon="☸",
    layout="centered"
)

st.title("👨🏻‍💻 RHP-GenAI Assistant")

# -------------------------------
# Initialize chat history
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# Display entire chat history
# -------------------------------
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# LLM
# -------------------------------
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

parser = StrOutputParser()

# -------------------------------
# User input
# -------------------------------
user_input = st.chat_input("Ask your doubts...")

if user_input:
    # Save user message
    st.session_state.chat_history.append(
        {"role": "user", "content": user_input}
    )

    # Build prompt with FULL history
    chat_prompt = [("system", "You are a helpful assistant")]

    for msg in st.session_state.chat_history:
        role = "human" if msg["role"] == "user" else "ai"
        chat_prompt.append((role, msg["content"]))

    prompt = ChatPromptTemplate.from_messages(chat_prompt)
    chain = prompt | llm | parser

    response = chain.invoke({})

    # Save assistant response
    st.session_state.chat_history.append(
        {"role": "assistant", "content": response}
    )

    # Force rerender (important)
    st.rerun()



