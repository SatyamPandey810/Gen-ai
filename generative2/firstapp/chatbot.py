from langchain_ollama import ChatOllama


model = ChatOllama(model="llama3.2")

chat_history = []

while True:
    user_input = input("You: ")
    chat_history.append(user_input)
    if user_input == "exit":
        break
    result = model.invoke(chat_history)
    chat_history.append(result.content)
    print("Ai :", result.content)

    print()

print("History :", chat_history)
