from langchain_ollama import ChatOllama


model = ChatOllama(model="llama3.2")

result = model.invoke("what is capital of india")

print(result.content)


