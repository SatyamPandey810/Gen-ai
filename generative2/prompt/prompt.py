from langchain_ollama import ChatOllama
import streamlit as st

st.header("Research Tools")

# Create LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

user_input = st.text_input("Enter your prompt")

if st.button("Summarize"):

    if user_input:
        response = llm.invoke(user_input)

        st.subheader("Response")
        st.write(response.content)

    else:
        st.warning("Please enter a prompt.")