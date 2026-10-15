from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_ollama import ChatOllama


model = ChatOllama(model="llama3.2")

messages = [
    SystemMessage(content="You are a helpfull assistant"),
    HumanMessage(content="Tell me about LangChain"),
]
result = model.invoke(messages)
messages.append(AIMessage(content=result.content))

print(messages)
