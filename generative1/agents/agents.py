from dotenv import load_dotenv

load_dotenv()

import os
import requests

from langchain.tools import tool
from langchain.agents import create_agent
from tavily import TavilyClient
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, ToolMessage


# -------------------------
# Weather Tool
# -------------------------


@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    if not API_KEY:
        return "Error: OPENWEATHER_API_KEY is not configured."

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if response.status_code != 200:
            return f"Error: {data.get('message', 'Something went wrong')}"

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        return f"Weather in {city}: {desc}, {temp}°C"

    except requests.RequestException as e:
        return f"Weather API error: {str(e)}"


# -------------------------
# Tavily Client
# -------------------------

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not configured.")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)


# -------------------------
# News/Search Tool
# -------------------------


@tool
def get_news(city: str) -> str:
    """Get the latest news about a city."""

    try:
        response = tavily_client.search(
            query=f"Latest news about {city}", search_depth="advanced", max_results=5
        )

        results = response.get("results", [])

        if not results:
            return f"No recent news found for {city}."

        news = []

        for result in results:
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            news.append(f"Title: {title}\nContent: {content}\nURL: {url}")

        return "\n\n".join(news)

    except Exception as e:
        return f"News search error: {str(e)}"


# -------------------------
# LLM
# -------------------------

llm = ChatOllama(model="llama3.2")

agent = create_agent(
    llm,
    tools=[get_weather, get_news],
    system_prompt="you are a helpfull city assistant.",
)
print("City agent | type exit to quit")

while True:
    user_input = input("You : ")
    if user_input.lower() == "exit":
        break
    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})
    
    final_message = result["messages"][-1]
    print("\nAgent:", final_message.content)
