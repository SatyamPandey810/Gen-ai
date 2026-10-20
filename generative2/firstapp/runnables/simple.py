from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings
from langchain.document_loaders import TextLoader
from langchain.vectorstores import FAISS



loader=TextLoader()
model = ChatOllama(model="llama3.2", temperature=0)

prompt = PromptTemplate(
    input_variables=["topic"], template="Suggest a catchy blog title about {topic}"
)

topic = input("Enter a topic :")

formatted_prompt = prompt.format(topic=topic)

blog_title = model.invoke(formatted_prompt)
print("Generated Blog Title :", blog_title)
