
from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_classic.chains import RetrievalQA


# 1. Load document
file_path = Path(
    "/home/satyam/Documents/genAI/generative2/firstapp/runnables/log.txt"
)

loader = TextLoader(str(file_path), encoding="utf-8")
docs = loader.load()

# 2. Split documents into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

chunks = splitter.split_documents(docs)

# 3. Initialize embedding model
embeddings = OllamaEmbeddings(
    model="nomic-embed-text"
)

# 4. Store chunks as vectors
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    collection_name="log_documents"
)

# 5. Create retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# 6. Initialize LLM
llm = ChatOllama(
    model="llama3.2",
    temperature=0
)

# 7. Create RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# 8. Ask a question
query = "What are the key takeaways from the document?"

answer = qa_chain.invoke({"query": query})

print("\nAnswer:")
print(answer["result"])

print("\nSource documents:")
for doc in answer["source_documents"]:
    print(doc.page_content)
    print("-" * 50)
