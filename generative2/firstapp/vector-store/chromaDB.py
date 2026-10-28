from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

# Create documents
doc1 = Document(
    page_content="Python is a high-level programming language used for AI, machine learning, automation, and web development.",
    metadata={"source": "python.txt", "topic": "Python"},
)

doc2 = Document(
    page_content="JavaScript is a programming language commonly used to build interactive web applications. Node.js allows JavaScript to run on the server.",
    metadata={"source": "javascript.txt", "topic": "JavaScript"},
)

doc3 = Document(
    page_content="React is a JavaScript library used to build reusable UI components. It supports component-based development and state management.",
    metadata={"source": "react.txt", "topic": "React"},
)

doc4 = Document(
    page_content="Node.js is a JavaScript runtime built on Chrome's V8 engine. It is commonly used to create scalable backend APIs.",
    metadata={"source": "nodejs.txt", "topic": "Backend"},
)

doc5 = Document(
    page_content="MongoDB is a NoSQL database that stores data in flexible BSON documents. It supports indexing, aggregation, and queries.",
    metadata={"source": "mongodb.txt", "topic": "Database"},
)

doc6 = Document(
    page_content="LangChain is a framework for developing applications powered by language models. It provides document loaders, retrievers, prompts, and chains.",
    metadata={"source": "langchain.txt", "topic": "GenAI"},
)

doc7 = Document(
    page_content="Ollama allows developers to run supported large language models locally. It can be integrated with LangChain to build AI applications.",
    metadata={"source": "ollama.txt", "topic": "GenAI"},
)

doc8 = Document(
    page_content="ChromaDB is a vector database used to store embeddings and retrieve semantically similar documents for RAG applications.",
    metadata={"source": "chromadb.txt", "topic": "Vector Database"},
)

doc9 = Document(
    page_content="Embeddings represent text as numerical vectors. Similar meanings can be represented by vectors that are close in embedding space.",
    metadata={"source": "embeddings.txt", "topic": "Embeddings"},
)

doc10 = Document(
    page_content="RAG combines document retrieval with a language model. It retrieves relevant information from a knowledge base and uses it to generate an answer.",
    metadata={"source": "rag.txt", "topic": "RAG"},
)

# Store all documents in a list
documents = [doc1, doc2, doc3, doc4, doc5, doc6, doc7, doc8, doc9, doc10]


# Create embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Store documents in ChromaDB
vector_store = Chroma.from_documents(
    documents=documents, embedding=embeddings, persist_directory="./chroma_db"
)

print("Documents stored successfully!")

# update the docs
updated_doc = Document(
    page_content="Python is widely used in AI, machine learning, automation, and backend development.",
    metadata={"topic": "Python", "version": 2},
)

vector_store.update_document(document_id="doc1", document=updated_doc)
print("Document updated!")

# # Search for similar documents
results = vector_store.similarity_search("what is python?", k=3)
print(results)


# for doc in results:
#     print("\nContent:", doc.page_content)
#     print("Metadata:", doc.metadata)
