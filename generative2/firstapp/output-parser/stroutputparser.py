from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

# Initialize Ollama model
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

# 1st prompt
template1 = PromptTemplate(
    template="Write a detailed report on {topic}",
    input_variables=["topic"]
)

# 2nd prompt
template2 = PromptTemplate(
    template="Write a 5-line summary of the following report:\n\n{text}",
    input_variables=["text"]
)

# First LLM call
prompt1 = template1.invoke({"topic": "black hole"})
result = llm.invoke(prompt1)


# Second LLM call
prompt2 = template2.invoke({"text": result.content})
result2 = llm.invoke(prompt2)

print("\n--- 5-Line Summary ---\n")
print(result2.content)