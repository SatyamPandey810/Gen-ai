from langchain_ollama import ChatOllama
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from rich import print


# 1. Creating a tool
@tool
def get_test_length(text: str) -> int:
    """Returns the number of characters in a given text."""
    return len(text)


# 2. Tool registry
tools = {
    "get_test_length": get_test_length
}


# 3. Creating LLM
llm = ChatOllama(model="llama3.2")


# 4. Binding tool to LLM
llm_with_tool = llm.bind_tools([get_test_length])


# 5. User message
messages = []

query = HumanMessage(
    content="Return the number of characters in the given text: 'Hello how are you'"
)

messages.append(query)


# 6. Ask LLM
result = llm_with_tool.invoke(messages)

messages.append(result)


# 7. Check whether LLM requested a tool
if result.tool_calls:

    tool_call = result.tool_calls[0]

    tool_name = tool_call["name"]
    tool_args = tool_call["args"]

    print("Tool Name:", tool_name)
    print("Tool Args:", tool_args)

    # 8. Execute the tool
    tool_result = tools[tool_name].invoke(tool_args)

    print("Tool Result:", tool_result)

    # 9. Send tool result back to LLM
    messages.append(
        ToolMessage(
            content=str(tool_result),
            tool_call_id=tool_call["id"]
        )
    )

    # 10. Get final answer
    final_result = llm_with_tool.invoke(messages)

    print("Final Answer:", final_result.content)