
from typing import TypedDict, Literal
from langchain_ollama import ChatOllama


# 1. Initialize the Ollama model
model = ChatOllama(
    model="llama3.2",
    temperature=0
)


# 2. Define the output schema
class Review(TypedDict):
    summary: str
    sentiment: Literal["positive", "negative", "mixed", "neutral"]


# 3. Create a structured-output model
structured_model = model.with_structured_output(
    Review,
    method="json_schema"
)


# 4. Provide the review
review_text = """
The hardware is great, but the software feels bloated.
There are too many pre-installed apps that I can't remove.
Also, the UI looks outdated compared to other brands.
Hoping for a software update to fix this.
"""


# 5. Invoke the model
result = structured_model.invoke(review_text)


# 6. Print the result
print(result)
print("Summary:", result["summary"])
print("Sentiment:", result["sentiment"])
