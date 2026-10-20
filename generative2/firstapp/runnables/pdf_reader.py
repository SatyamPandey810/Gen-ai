from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

file_path = Path("/home/satyam/Documents/genAI/generative2/firstapp/runnables/log.txt")
loader = TextLoader(str(file_path))
docs = loader.load()

# 2. Split the documents into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# 3. Initialize embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

vectorstore = FAISS.from_documents(chunks, embeddings)

# 4. Create retriever and use .invoke() instead of get_relevant_documents()
retriever = vectorstore.as_retriever()
query = "where is room door?"
retrieved_docs = retriever.invoke(query)
3
# 5. Combine the retrieved text content
retrieved_text = "\n".join([doc.page_content for doc in retrieved_docs])

# 6. Initialize the LLM and generate the answer
model = ChatOllama(model="llama3.2", temperature=0)
prompt = f"Based on the following text, answer the question: {query}\n\n{retrieved_text}"
answer = model.invoke(prompt)

# Print the text content from the AIMessage response
print("Answer:", answer.content)