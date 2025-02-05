import os
import requests
from dotenv import load_dotenv

# Load credentials
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
EXPENSES_DB_ID = os.getenv("EXPENSES_DB_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Notion-Version": "2022-06-28"
}

def fetch_database_schema():
    """Fetches the database schema to confirm property names."""
    url = f"https://api.notion.com/v1/databases/{EXPENSES_DB_ID}"
    response = requests.get(url, headers=HEADERS)

    print(f"🔍 Response Code: {response.status_code}")
    print(f"🔍 Response Text: {response.text}")

fetch_database_schema()