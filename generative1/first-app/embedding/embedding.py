from langchain_ollama import OllamaEmbeddings

embeddings = OllamaEmbeddings(model="nomic-embed-text")

text = [
    "Hello this is satyam pandey",
    "Hello what is your name",
    "And you all are very beautiful",
]


# result = embeddings.embed_query("What is cricket?")
result = embeddings.embed_documents(text)


print(result)
print("Vector dimensions:", len(result))
