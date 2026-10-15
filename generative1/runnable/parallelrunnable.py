from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
# 1. prompt template

# 2. model
model = ChatOllama(model="llama3.2")
# 3. Output parser
parser = StrOutputParser()
short_prompt = ChatPromptTemplate.from_template("Explain {topic} in 1-2 lines")
detailed_prompt = ChatPromptTemplate.from_template("Explain {topic} in detail")
topic = "Machine Learning"

chain = RunnableParallel({
    "Short": short_prompt | model | parser,
    "detailed": detailed_prompt | model | parser,
})

result = chain.invoke({"topic": "Machine learning"})
print(result,"short---->",["Short"])
print(result,"detailed---->",["detailed"])
