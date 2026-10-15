from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate

embedding_model = OllamaEmbeddings(model="nomic-embed-text")
vectorStore = Chroma(persist_directory="chroma-db", embedding_function=embedding_model)

retriever = vectorStore.as_retriever(
    search_type="mmr", search_kwargs={"k": 4, "fetch_k": 10, "lambda_mult": 0.5}
)

model = ChatOllama(
    model="llama3.2"
)


# prompt templete
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpfull AI assistant.add()
         Use ONLY the provided context to answer the question.
         
         If the answer is not present in the context,
         say:"I could not find the answer in the document.
        """,
        ),
        (
            "human",
            """Context:
            {context}
            
            Question:
            {question}
            """,
        ),
    ]
)

print("Rag system created")
print("press 0 to exit")

while True:
    query = input("You : ")
    if query == "0":
        break
    docs = retriever.invoke(query)

    context = "\n\n".join([doc.page_content for doc in docs])

    final_prompt = prompt.invoke({"context": context, "question": query})

    response = model.invoke(final_prompt)
    print(f"\n AI: {response.content}")
