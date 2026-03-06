#!/usr/bin/env python3
import os
import requests
from fastmcp import FastMCP

mcp = FastMCP("Reflect MCP Server", stateless_http=True, json_response=True)

REFLECT_TOKEN = os.environ["REFLECT_TOKEN"]
GRAPH_ID = os.environ["REFLECT_GRAPH_ID"]
HEADERS = {"Authorization": f"Bearer {REFLECT_TOKEN}"}
BASE = f"https://reflect.app/api/v1/graphs/{GRAPH_ID}"

@mcp.tool(description="Append text to the [[Inbox]] list in today's daily note in Reflect")
def append_to_daily_note(text: str) -> str:
    response = requests.put(
        f"{BASE}/daily-notes",
        headers=HEADERS,
        json={
            "text": text,
            "transform_type": "list-append",
            "list_name": "[[Inbox]]"
        }
    )
    return "Appended to Inbox!" if response.ok else f"Failed: {response.status_code} {response.text}"

@mcp.tool(description="Create a new note in Reflect with a title and content")
def create_note(title: str, content: str) -> str:
    response = requests.post(
        f"{BASE}/notes",
        headers=HEADERS,
        json={
            "subject": title,
            "content_markdown": content
        }
    )
    return "Note created!" if response.ok else f"Failed: {response.status_code} {response.text}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"

    print(f"Starting Reflect MCP Server on {host}:{port}")

    mcp.run(
        transport="streamable-http",
        host=host,
        port=port,
        stateless_http=True
    )
