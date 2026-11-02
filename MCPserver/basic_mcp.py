from fastmcp import FastMCP

mcp = FastMCP(name="Simple MCP Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """"Accept two numbers and return sum of those numbers"""
    return a + b
  
 ##### Transport => stdio (standard input and output), http
mcp.run(transport="streamable-http")




