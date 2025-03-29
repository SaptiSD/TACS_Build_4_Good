import os
import re
import requests

NOTION_API_URL = "https://api.notion.com/v1/"
#DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
#NOTION_TOKEN = os.getenv("NOTION_TOKEN")

NOTION_TOKEN = "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"
DATABASE_ID = "1c5cc172039980b9902ac96a2aaecc65"

HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_child_blocks(page_id):
    """
    Retrieves child blocks (tasks) for a given goal page.
    Parses the text to extract the task title and due date assuming the format "Task Title (Due: YYYY-MM-DD)".
    """
    url = NOTION_API_URL + f"blocks/{page_id}/children?page_size=100"
    response = requests.get(url, headers=HEADERS)
    tasks = []
    if response.ok:
        children = response.json().get("results", [])
        for child in children:
            if child.get("type") == "to_do":
                rich_texts = child["to_do"].get("rich_text", [])
                if rich_texts:
                    text_content = rich_texts[0]["text"]["content"]
                    # Use regex to extract task title and due date
                    match = re.match(r"^(.*?) \(Due:\s*(.*?)\)$", text_content)
                    if match:
                        task_title = match.group(1)
                        task_due_date = match.group(2)
                    else:
                        task_title = text_content
                        task_due_date = ""
                    tasks.append({
                        "task_title": task_title,
                        "task_due_date": task_due_date
                    })
        return tasks
    else:
        print("Error retrieving child blocks for page", page_id, response.text)
        return []

def query_database():
    """
    Queries the Notion database for all goal pages.
    For each goal, it retrieves its child blocks (tasks) using get_child_blocks().
    Returns a list of dictionaries with goal details and their tasks.
    """
    url = NOTION_API_URL + f"databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=HEADERS)
    data = []
    if response.ok:
        results = response.json().get("results", [])
        for page in results:
            properties = page.get("properties", {})
            name_prop = properties.get("Name", {})
            due_prop = properties.get("Due Date", {})
            goal_title = "Untitled"
            if name_prop.get("title"):
                goal_title = name_prop["title"][0]["text"]["content"]
            goal_due_date = due_prop.get("date", {}).get("start", "")
            page_id = page.get("id")
            tasks = get_child_blocks(page_id)
            data.append({
                "goal_title": goal_title,
                "goal_due_date": goal_due_date,
                "tasks": tasks
            })
        return data
    else:
        print("Error querying database:", response.text)
        return []
