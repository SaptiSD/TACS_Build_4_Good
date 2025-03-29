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

def delete_page(page_id):
    """
    Deletes the specified page/block in Notion.
    """
    url = NOTION_API_URL + f"blocks/{page_id}"
    response = requests.delete(url, headers=HEADERS)
    if response.ok:
        return True
    else:
        print("Error deleting page:", response.text)
        return False
