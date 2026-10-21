from langchain_community.document_loaders import TextLoader
from pathlib import Path

from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


model = ChatOllama(model="llama3.2", temperature=0)
prompt = PromptTemplate(
    template="Write a summary for the following poem - \n {poem}",
    input_variables=["poem"],
)

parser = StrOutputParser()

file_path = Path(
    "/home/satyam/Documents/genAI/generative2/firstapp/document-loaders/log.txt"
)
loader = TextLoader(str(file_path), encoding="utf-8")
docs = loader.load()

chain = prompt | model | parser

result = chain.invoke({"poem": docs[0].page_content})
print(result)
