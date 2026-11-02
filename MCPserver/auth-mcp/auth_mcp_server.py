
import os
from fastmcp import FastMCP
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token

JWT_SECRET_KEY = "f55aeea7-0d02-40be-a9b1-c7c675479979"
JWT_ALGO = "HS256"
JWT_ISSUER = "http://localhost:8001"
JWT_AUDIENCE = "my-mcp-server"

verifier = JWTVerifier(
    public_key=JWT_SECRET_KEY,
    algorithm=JWT_ALGO,
    issuer=JWT_ISSUER,
    audience=JWT_AUDIENCE,
)

mcp = FastMCP(
    "Secure MCP Server",
    auth=verifier
)


@mcp.tool()
def whoami() -> dict:
    """Returns the userid of the current authenticated user."""

    token = get_access_token()

    print("Authenticated token:", token)

    return {
        "client_id": token.client_id,
        "email": token.claims.get("email","")
    }


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
        path="/mcp"
    )
