#!/usr/bin/env python3
import os
import requests
from fastmcp import FastMCP

mcp = FastMCP("Reflect MCP Server")

@mcp.tool(description="Append text to today's daily note in Reflect")
def append_to_reflect(text: str) -> str:
    token = os.environ["REFLECT_TOKEN"]
    graph_id = os.environ["REFLECT_GRAPH_ID"]

    response = requests.put(
        f"https://reflect.app/api/v1/graphs/{graph_id}/daily-notes",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "text": text,
            "transform_type": "list-append"
        }
    )
    return "Appended to Reflect!" if response.ok else f"Failed: {response.status_code} {response.text}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"

    print(f"Starting Reflect MCP Server on {host}:{port}")

    mcp.run(
        transport="http",
        host=host,
        port=port,
        stateless_http=True
    )
