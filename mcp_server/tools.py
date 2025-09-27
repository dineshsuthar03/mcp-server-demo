# tools.py
from typing import Dict

# In-memory DB
users_db = []

# Tool: create_user
async def create_user(payload: Dict):
    """
    payload: {"name": str, "mobile": str, "age": int}
    """
    users_db.append(payload)
    return {"status": "success", "user": payload}

# Tool: get_user
async def get_user(payload: Dict):
    """
    payload: {"name": str (optional), "id": int (optional)}
    """
    if "name" in payload:
        for user in users_db:
            if user["name"] == payload["name"]:
                return {"status": "success", "user": user}
        return {"status": "not_found"}
    return {"status": "all_users", "users": users_db}

# Map tool names to functions
TOOL_FUNCTIONS = {
    "create_user": create_user,
    "get_user": get_user
}
