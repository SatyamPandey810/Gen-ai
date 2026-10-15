from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

search_tool = TavilySearch(max_results=5)

llm = ChatOllama(model="llama3.2")

prompt = ChatPromptTemplate.from_template(
    """
    You are a helpful assistant.

    Summarize the following news into clear bullet points.

    {news}
    """
)
 
chain = prompt | llm | StrOutputParser()
news_result = search_tool.invoke(
    {"query": "Latest AI news of 2026"}
)

result = chain.invoke({"news": news_result})
print(result)