import calendar
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

# Load API credentials
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
EXPENSES_DB_ID = os.getenv("EXPENSES_DB_ID")
CATEGORIES_DB_ID = os.getenv("CATEGORIES_DB_ID")
MONTHLY_REPORTS_DB_ID = os.getenv("MONTHLY_REPORTS_DB_ID")
SUBSCRIPTIONS_DB_ID = os.getenv("SUBSCRIPTIONS_DB_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# For test purposes
def fetch_database_entries(database_id):
    """Fetch all entries from a given Notion database."""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=HEADERS)

    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"❌ Error fetching database {database_id}: {response.text}")
        return []

# Fetch Expenses Data
def get_expenses_for_month(year, month):
    """Fetch expenses for a specific month from Notion."""
    # Get the last day of the month dynamically
    _, last_day = calendar.monthrange(year, month)
    
    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{last_day:02d}"
    print(f"📅 Fetching expenses from {start_date} to {end_date}...")
    url = f"https://api.notion.com/v1/databases/{EXPENSES_DB_ID}/query"

    query_payload = {
        "filter": {
            "and": [
                {
                    "property": "Date",
                    "date": {"on_or_after": start_date}
                },
                {
                    "property": "Date",
                    "date": {"on_or_before": end_date}
                }
            ]
        }
    }

    response = requests.post(url, headers=HEADERS, json=query_payload)
    
    if response.status_code == 200:
        expenses = response.json()["results"]
        expense_data = []
        
        for item in expenses:
            # Extract properties safely with default values
            title = item["properties"].get("Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown")
            amount = item["properties"].get("Amount", {}).get("number", 0)  # Default to 0 if missing
            date = item["properties"].get("Date", {}).get("date", {}).get("start", "Unknown Date")
            category = item["properties"].get("Category", {}).get("select", {}).get("name", "Uncategorized")
            
            # Append expense data even if some fields are missing
            expense_data.append({
                "title": title,
                "amount": amount,
                "date": date,
                "category": category,
                "id": item.get("id", "No ID")  # Default to "No ID" if missing
            })

        return expense_data
    else:
        print(f"❌ Error fetching expenses: {response.text}")
        return []

# Fetch Categories Data
def get_categories():
    categories = fetch_database_entries(CATEGORIES_DB_ID)
    category_list = []
    for item in categories:
        try:
            category_name = item["properties"]["Name"]["title"][0]["text"]["content"]
            budget = item["properties"]["Budget"]["number"]
            category_list.append({"category": category_name, "budget": budget})
        except KeyError:
            continue
    return category_list

#Fetch Subscriptions Data
def get_subscriptions():
    subscriptions = fetch_database_entries(SUBSCRIPTIONS_DB_ID)
    subscription_list = []
    for item in subscriptions:
        try:
            subscription_name = item["properties"]["Name"]["title"][0]["text"]["content"]
            cost = item["properties"]["Cost"]["number"]
            subscription_list.append({"subscription": subscription_name, "cost": cost})
        except KeyError:
            continue
    return subscription_list

# Write Monthly Report to Notion
def write_report_to_notion(year, month, report_text, expenses):
    """Creates a Monthly Report in Notion and links filtered expenses using a relation property."""
    current_month = f"{year}-{month:02d}"

    url = "https://api.notion.com/v1/pages"

    # Extract Expense IDs to link them in the relation property
    expense_ids = [{"id": expense["id"]} for expense in expenses]

    data = {
        "parent": {"database_id": os.getenv("MONTHLY_REPORTS_DB_ID")},
        "properties": {
            "Name": {"title": [{"text": {"content": f"{current_month} Summary"}}]},
            "Report Notes": {"rich_text": [{"text": {"content": report_text}}]},
            "Related Expense": {"relation": expense_ids}  # Linking expenses
        }
    }

    response = requests.post(url, headers=HEADERS, json=data)

    if response.status_code == 200:
        print(f"✅ Monthly Report for {current_month} created successfully with related expenses!")
    else:
        print(f"❌ Error creating report: {response.text}")


def get_all_expenses():
    """Fetch all expenses from Notion without filtering."""
    url = f"https://api.notion.com/v1/databases/{EXPENSES_DB_ID}/query"
    
    response = requests.post(url, headers=HEADERS)
    
    print(f"🔍 Response Code: {response.status_code}")
    print(f"🔍 Response Text: {response.text[:500]}")  # Print only first 500 characters

    if response.status_code == 200:
        expenses = response.json()["results"]
        print(f"✅ Retrieved {len(expenses)} total expenses.")
        return expenses
    else:
        print(f"❌ Error fetching expenses: {response.text}")
        return []