from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text = [
    "Hello this is satyam pandey",
    "Hello what is your name",
    "And you all are very beautiful",
]


# result = embeddings.embed_query("What is cricket?")
result = embedding.embed_documents(text)
print(result)
