from fastmcp import FastMCP

mcp = FastMCP(name="Send email MCP Server")

sender_email = "satyampandeyrewa810@gmail.com"
pasword = "your_app_password"


def _send(email: str, subject: str, body: str) -> str:
    receiver_email = email
