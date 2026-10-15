from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

data = PyMuPDFLoader("documents-loadders/AWS.pdf")
docs = data.load()
# splitter = TokenTextSplitter(chunk_size=100, chunk_overlap=10)
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=10)

chunks=splitter.split_documents(docs)

print(len(chunks))
print(chunks)