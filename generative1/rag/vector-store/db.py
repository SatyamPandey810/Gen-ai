from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document

docs = [
    Document(
        page_content="Python is widly used in Artificial Intellingenvce",
        metadata={"source": "AI_book"},
    ),
    Document(
        page_content="Pandas is used for data analysis in python",
        metadata={"source": "DataScience_book"},
    ),
    Document(
        page_content="Neural networks are used in deep learning",
        metadata={"source": "DL_book"},
    ),
]

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma.from_documents(
    documents=docs, embedding=embeddings, persist_directory="chroma-db"
)
result = vectorstore.similarity_search("what is used for data analysis?", k=2)

for r in result:
    print(r)

retriver = vectorstore.as_retriever()
docs=retriver.invoke("Explain deep learning")

for d in docs:
    print(d.page_content)
