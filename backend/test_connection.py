import os
import requests
from dotenv import load_dotenv

# Load API credentials from .env
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")

# Define Notion API headers
headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def test_notion_connection():
    """Fetches data from the Notion database and prints the results"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("✅ Connection Successful! Retrieved data:")
        
        # Extracting and displaying database entries
        for entry in data["results"]:
            page_id = entry["id"]
            page_title = entry["properties"]["Name"]["title"][0]["text"]["content"]
            print(f"Page ID: {page_id} | Title: {page_title}")

    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

# Run the test
if __name__ == "__main__":
    test_notion_connection()