import os
import smtplib
from email.message import EmailMessage

from fastmcp import FastMCP

mcp = FastMCP(name="Send email MCP Server")

SENDER_EMAIL = os.environ["SENDER_EMAIL"]
APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]


def _send(email: str, subject: str, body: str) -> str:
    msg = EmailMessage()
    msg["From"] = SENDER_EMAIL
    msg["To"] = email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.send_message(msg)

    return f"Email sent to {email}"


@mcp.tool()
def send_email(email: str, subject: str, body: str) -> str:
    """Send a plain-text email to the given address."""
    try:
        return _send(email, subject, body)
    except Exception as e:
        return f"Failed to send email: {e}"


if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="0.0.0.0", port=8000, path="/mcp")