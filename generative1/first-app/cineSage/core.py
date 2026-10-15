from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

model = ChatOllama(
    model="llama3.2"
)

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

paragraph =input("Give your paragraph :")
messages = prompt.invoke({
    "paragraph": paragraph
})

response = model.invoke(messages)
print(response.content)