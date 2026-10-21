
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from pathlib import Path

file_path = Path(
    "/home/satyam/Documents/genAI/generative2/firstapp/document-loaders/dir"
)
loader = DirectoryLoader(str(file_path), glob="**/*.pdf", loader_cls=PyPDFLoader)
# docs = loader.load()
docs = loader.lazy_load()

for document in docs:
    print(document)


# print(len(docs))
# print(docs)