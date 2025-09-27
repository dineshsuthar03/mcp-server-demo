# router.py
import os
import json
import re
from dotenv import load_dotenv
from openai import AzureOpenAI
from .tools import TOOL_FUNCTIONS

load_dotenv()  # Load .env file

# Azure OpenAI client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

MODEL = os.getenv("AZURE_OPENAI_MODEL")
TEMPERATURE = float(os.getenv("AZURE_OPENAI_TEMPERATURE", 0.3))
MAX_TOKENS = int(os.getenv("AZURE_OPENAI_MAX_TOKENS", 4000))


def safe_json_extract(text: str):
    """
    Safely extract JSON from LLM response.
    Handles markdown/code blocks or plain JSON.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Attempt to extract JSON from text
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError(f"Unable to parse JSON from LLM response: {text}")


async def route_query(user_query: str):
    """
    MCP routing:
    1. Ask Azure OpenAI which tool to call + payload
    2. Safely parse JSON
    3. Call Python function directly
    """
    system_prompt = """
    You are an MCP assistant.
    Based on the user query, select the correct tool and provide payload.
    ALWAYS respond in valid JSON ONLY in the format:
    {
        "tool": "tool_name",
        "payload": { ... }
    }
    Do NOT include extra text.
    """

    try:
        # Async call to Azure OpenAI
        response = await client.chat.completions.acreate(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_query}
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        raw_text = response["choices"][0]["message"]["content"]

        # Safe JSON parsing
        try:
            tool_data = safe_json_extract(raw_text)
        except ValueError as e:
            return {"status": "error", "message": str(e), "raw_response": raw_text}

        tool_name = tool_data.get("tool")
        payload = tool_data.get("payload", {})

        if tool_name not in TOOL_FUNCTIONS:
            return {"status": "error", "message": f"Unknown tool: {tool_name}"}

        # Call the tool directly
        tool_func = TOOL_FUNCTIONS[tool_name]
        result = await tool_func(payload)

        return {
            "status": "success",
            "tool": tool_name,
            "payload": payload,
            "result": result
        }

    except Exception as exc:
        return {
            "status": "error",
            "message": f"Unexpected error: {str(exc)}"
        }
