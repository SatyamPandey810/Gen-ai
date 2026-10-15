from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser


# Initialize Ollama model
model = ChatOllama(model="llama3.2", temperature=0)

# 1st prompt
template1 = PromptTemplate(
    template="Write a detailed report on {topic}", input_variables=["topic"]
)

# 2nd prompt
template2 = PromptTemplate(
    template="Write a 5-line summary of the following report:\n\n{text}",
    input_variables=["text"],
)

parser = StrOutputParser()
chain = template1 | model | parser | template2 | model | parser

result=chain.invoke({'topic':'love'})
print(result)