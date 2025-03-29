import os
import requests

# Get your Notion API token and Database ID from environment variables
NOTION_API_URL = "https://api.notion.com/v1/"
#NOTION_TOKEN = os.getenv("NOTION_TOKEN")  # Set this in your .env file
#DATABASE_ID = os.getenv("NOTION_DATABASE_ID")  # Set this in your .env file

NOTION_TOKEN = "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"
DATABASE_ID = "1c5cc172039980b9902ac96a2aaecc65"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def create_goal(title, due_date):
    """
    Creates a goal as a new page in the Notion database.
    """
    url = NOTION_API_URL + "pages"
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": title}}]},
            "Due Date": {"date": {"start": due_date}}
        }
    }
    response = requests.post(url, headers=HEADERS, json=data)
    if response.ok:
        result = response.json()
        return result.get("id")
    else:
        print("Error creating goal:", response.text)
        return None

def create_task(goal_id, task_title, task_due_date):
    """
    Adds a task as a child block (to_do) under the specified goal page.
    The task text is formatted as "Task Title (Due: YYYY-MM-DD)".
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
        print("Error creating task:", response.text)
        return False
