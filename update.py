import os
import requests

NOTION_API_URL = "https://api.notion.com/v1/"
#NOTION_TOKEN = os.getenv("NOTION_TOKEN")

NOTION_TOKEN = "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"
DATABASE_ID = "1c5cc172039980b9902ac96a2aaecc65"

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
