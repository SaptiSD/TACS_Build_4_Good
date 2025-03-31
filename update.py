import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file in development
if os.path.exists('.env'):
    load_dotenv()

# Get Notion API configuration from environment variables with fallback error messages
NOTION_API_URL = os.getenv("NOTION_API_URL")
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("DATABASE_ID")

# Validate required environment variables
if not all([NOTION_API_URL, NOTION_TOKEN, DATABASE_ID]):
    raise ValueError("Missing required environment variables. Please check NOTION_API_URL, NOTION_TOKEN, and DATABASE_ID are set.")

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def update_goal_with_task(goal_id, task_title, task_due_date):
    """
    Adds an additional task as a child block under the goal.
    """
    url = NOTION_API_URL + f"blocks/{goal_id}/children"
    data = {
        "children": [
            {
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [
                        {"text": {"content": f"{task_title} (Due: {task_due_date})"}}
                    ],
                    "checked": False
                }
            }
        ]
    }
    response = requests.patch(url, headers=HEADERS, json=data)
    if response.ok:
        return True
    else:
        print("Error updating goal with task:", response.text)
        return False
