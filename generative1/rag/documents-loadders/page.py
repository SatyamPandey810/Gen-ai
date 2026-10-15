from langchain_community.document_loaders import WebBaseLoader

url = "http://satyam.space"
data = WebBaseLoader(url)

docs = data.load()
print(len(docs))

print(docs[0].page_content)

print(docs[0].metadata)