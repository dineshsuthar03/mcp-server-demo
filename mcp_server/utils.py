# utils.py
import json
import re

def safe_json_extract(text: str):
    """
    Tries to parse JSON from a string.
    If LLM wraps JSON in text or markdown, extract the JSON part.
    """
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError(f"Unable to parse JSON from LLM response: {text}")
