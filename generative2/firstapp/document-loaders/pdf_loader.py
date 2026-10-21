from langchain_community.document_loaders import PyPDFLoader
from pathlib import Path


file_path = Path(
    "/home/satyam/Documents/genAI/generative2/firstapp/document-loaders/AWS.pdf"
)
loader = PyPDFLoader(str(file_path))
docs = loader.load()

print(len(docs))