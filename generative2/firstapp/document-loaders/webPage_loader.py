from langchain_community.document_loaders import WebBaseLoader


from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate


model = ChatOllama(model="llama3.2", temperature=0)
prompt = PromptTemplate(
    template="Answer the following question \n {question} from the following text \n {text}",
    input_variables=["question", "text"],
)
parser = StrOutputParser()


url = "https://www.flipkart.com/laptops/apple~brand/pr?sid=6bo,b5g"

loader = WebBaseLoader(
    web_paths=(url,), requests_kwargs={"timeout": 20}, raise_for_status=True
)

docs = loader.load()

# print("Total documents:", len(docs))

# for doc in docs:
#     print("Metadata:", doc.metadata)
#     print("Page content:", doc.page_content[:2000])

chain = prompt | model | parser

result=chain.invoke({'question':'What is the peak birghtness of this product?','text':docs[0].page_content})

print(result)