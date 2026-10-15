from langchain_community.document_loaders import TextLoader

data=TextLoader("documents-loadders/log.txt")

documents = data.load()
print(documents)