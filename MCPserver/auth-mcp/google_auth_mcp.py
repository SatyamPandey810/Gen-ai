
MCP_SERVER_URL = "http://localhost:8000"
import os

from fastmcp.server.auth.providers.google import GoogleProvider
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token

verifier = GoogleProvider(
    client_id=GOOGLE_CLIENT_ID,
    client_secret=GOOGLE_CLIENT_SECRET,
    base_url=MCP_SERVER_URL,
)

mcp = FastMCP("Secure MCP Server", auth=verifier)


@mcp.tool()
def whoami() -> dict:
    """Returns the userid of the current authenticated user."""

    token = get_access_token()

    print("Authenticated token:", token)
    return {
        "client_id": token.client_id,
    }

@mcp.tool
def send_email_tool(email: str, subject: str, body: str):
    "Send email to any email address. Just required receiver email address, subject and body"
    return f"Email sent to {email}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, path="/mcp")
