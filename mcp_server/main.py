# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from .router import route_query
from .tools import TOOL_FUNCTIONS

app = FastAPI(title="MCP Server - Function Based")

# Pydantic model for /mcp/route
class PromptRequest(BaseModel):
    query: str

@app.post("/mcp/route")
async def mcp_route(req: PromptRequest):
    return await route_query(req.query)

@app.get("/mcp/tools")
async def list_tools():
    return {
        "tools": [
            {"name": name, "inputs": {}, "description": f"Python function {name}"}
            for name in TOOL_FUNCTIONS
        ]
    }
