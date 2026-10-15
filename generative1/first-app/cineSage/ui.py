import streamlit as st

from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# -----------------------------
# Model
# -----------------------------

model = ChatOllama(
    model="llama3.2"
)


# -----------------------------
# Prompt
# -----------------------------

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are CineSage, an intelligent movie information extraction assistant.

Analyze the given movie-related paragraph and extract useful information.

Follow these rules:

- Do not invent information that is not present in the paragraph.
- If some information is not available, write "Not mentioned".
- Keep the extracted information concise and useful.
- Provide a short summary at the end.
- Use clear headings and bullet points.
- Do not return JSON.
- Do not use markdown tables.

Extract the following information:

Movie Name:
Genre:
Cast:
Characters:
Director:
Main Plot:
Setting:
Themes:
Tone:
Key Takeaway:
Keywords:

Quick Summary:
Write a concise 2-3 sentence summary of the paragraph.

Here is the paragraph:

{paragraph}
"""
    ),
    (
        "human",
        "Extract the movie information from the paragraph."
    )
])


# -----------------------------
# Chain
# -----------------------------

chain = prompt | model


# -----------------------------
# Streamlit UI
# -----------------------------

st.title("🎬 CineSage")

st.subheader("Movie Information Extraction")

paragraph = st.text_area(
    "Enter your movie paragraph:",
    height=250
)


if st.button("Extract Information"):

    if paragraph:

        with st.spinner("Analyzing..."):

            response = chain.invoke({
                "paragraph": paragraph
            })

        st.subheader("Extracted Information")

        st.write(response.content)

    else:
        st.warning("Please enter a paragraph.")