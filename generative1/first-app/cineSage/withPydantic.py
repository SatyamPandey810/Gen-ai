from typing import Optional, List

from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

load_dotenv()


class Movie(BaseModel):
    title: str
    release_year: Optional[int] = None
    genre: List[str]
    cast: List[str]
    rating: Optional[float] = None
    summary: str


parser = PydanticOutputParser(pydantic_object=Movie)

model = ChatOllama(
    model="llama3.2"
)

prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are a movie information extraction assistant.

Extract movie information from the given paragraph.

{format_instructions}

Do not add any information that is not present in the paragraph.
If release year or rating is not mentioned, return null.
"""
    ),
    (
        "human",
        "{paragraph}"
    )
])


paragraph = input("Give your paragraph: ")

messages = prompt.invoke({
    "paragraph": paragraph,
    "format_instructions": parser.get_format_instructions()
})

response = model.invoke(messages)

print(response.content)

movie = parser.parse(response.content)

print("\nParsed Movie:")

print(movie)