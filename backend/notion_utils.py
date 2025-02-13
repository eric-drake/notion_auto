import calendar
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
import aiohttp
import asyncio

# Load API credentials
load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
EXPENSES_DB_ID = os.getenv("EXPENSES_DB_ID")
CATEGORIES_DB_ID = os.getenv("CATEGORIES_DB_ID")
MONTHLY_REPORTS_DB_ID = os.getenv("MONTHLY_REPORTS_DB_ID")
SUBSCRIPTIONS_DB_ID = os.getenv("SUBSCRIPTIONS_DB_ID")
MONTH_EXPENSE_DB_ID = os.getenv("MONTH_EXPENSE_DB_ID")
MONTH_INCOME_DB_ID = os.getenv("MONTH_INCOME_DB_ID")

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}


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
def get_expenses_for_month(year, month, category_list):
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
            title = item["properties"].get("Expense", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown")
            amount = item["properties"].get("Amount", {}).get("number", 0)  # Default to 0 if missing
            date = item["properties"].get("Date", {}).get("date", {}).get("start", "Unknown Date")
            category_id = item["properties"].get("Categories", {}).get("relation", [{}])[0].get("id", None)
            category_name = get_category_name(category_id, category_list)
            
            
            # Append expense data even if some fields are missing
            expense_data.append({
                "title": title,
                "amount": amount,
                "date": date,
                "category": category_name,
                "id": item.get("id", "No ID")  # Default to "No ID" if missing
            })
        # Fetch subscriptions and add them to the expenses
        subscriptions = get_subscriptions()
        for subscription in subscriptions:
            if subscription['status'] == 'Active':
                expense_data.append(
                    {
                        'title': subscription['subscription']+' Subscription',
                        'amount': subscription['cost'],
                        'date': f"{year}-{month:02d}-01",
                        'category': 'Subscription',
                        'id': 'No ID'
                    }
                )

        return expense_data
    else:
        print(f"❌ Error fetching expenses: {response.text}")
        return []

# Get category name from category id, used in get_expenses_for_month
def get_category_name(category_id, category_list):
    """Fetch the category name from the pre-fetched category list."""
    for category in category_list:
        if category["id"] == category_id:
            return category["category"]
    return "Uncategorized"
    
# Fetch Categories Data
def get_categories():
    categories = fetch_database_entries(CATEGORIES_DB_ID)
    category_list = []
    for item in categories:
        try:
            category_name = item["properties"]["Category"]["title"][0]["text"]["content"]
            budget = item["properties"]["Monthly Budget"]["number"]
            id = item["id"]
            category_list.append({"id":id, "category": category_name, "budget": budget})

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
            monthly_cost = item["properties"]["Monthly Cost"]['formula']["number"]
            status = item["properties"]["Status"]["select"]["name"]
            subscription_list.append({"subscription": subscription_name, "cost": monthly_cost, "status": status})
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

# def get_all_expenses():
#     """Fetch all expenses from Notion without filtering."""
#     url = f"https://api.notion.com/v1/databases/{EXPENSES_DB_ID}/query"
    
#     response = requests.post(url, headers=HEADERS)
    
#     print(f"🔍 Response Code: {response.status_code}")
#     print(f"🔍 Response Text: {response.text[:500]}")  # Print only first 500 characters

#     if response.status_code == 200:
#         expenses = response.json()["results"]
#         print(f"✅ Retrieved {len(expenses)} total expenses.")
#         return expenses
#     else:
#         print(f"❌ Error fetching expenses: {response.text}")
#         return []
    
'''For add expense into the month expense database
    - add_expense: gather the expense to be added to database
    - add_expenses_to_month_expense: Add multiple expenses to the month expense database
    - clear_month_expense: Delete all entries in the month expense database
    - clear_month_expense_sync: Synchronous version of clear_month_expense, for directly calling from other scripts
    - add_expenses_to_month_expense_sync: Synchronous version of add_expenses_to_month_expense, for directly calling from other scripts
'''
async def add_expense(session, expense,retries=3, backoff_in_seconds=1):
    title = expense.get("title", "Untitled Expense")
    amount = expense.get("amount", 0)
    date = expense.get("date", "Unknown Date")
    category = expense.get("category", "Uncategorized")

    payload = {
        "parent": {"database_id": MONTH_EXPENSE_DB_ID},
        "properties": {
            "Expense": {"title": [{"text": {"content": title}}]},
            "Amount": {"number": amount},
            "Date": {"date": {"start": date}},
            "Categories": {"select": {"name": category}}
        }
    }

    for attempt in range(retries):
        async with session.post("https://api.notion.com/v1/pages", headers=HEADERS, json=payload) as response:
            if response.status == 200:
                print(f"✅ Added expense: {title} - ${amount}")
                return
            elif response.status == 409:  # Conflict error
                print(f"⚠️ Conflict error adding expense: {title}. Retrying...")
                await asyncio.sleep(backoff_in_seconds * (2 ** attempt))  # Exponential backoff
            else:
                print(f"❌ Error adding expense: {await response.text()}")
                return

    print(f"❌ Failed to add expense after {retries} attempts: {title}")

async def add_expenses_to_month_expense(expenses):
    """Adds the filtered expenses into the 'Month Expense' database."""
    async with aiohttp.ClientSession() as session:
        tasks = [add_expense(session, expense) for expense in expenses]
        await asyncio.gather(*tasks) 

def add_expenses_to_month_expense_sync(expenses):
    asyncio.run(add_expenses_to_month_expense(expenses))

async def clear_month_expense():
    """Deletes all entries in the 'Month Expense' database."""
    url = f"https://api.notion.com/v1/databases/{MONTH_EXPENSE_DB_ID}/query"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=HEADERS) as response:
            if response.status == 200:
                data = await response.json()
                pages = data["results"]
                tasks = []
                for page in pages:
                    delete_url = f"https://api.notion.com/v1/pages/{page['id']}"
                    tasks.append(session.patch(delete_url, headers=HEADERS, json={"archived": True}))
                await asyncio.gather(*tasks)
                print(f"✅ Cleared {len(pages)} old expenses from Month Expense.")
            else:
                print(f"❌ Error fetching Month Expense data: {await response.text()}")

def clear_month_expense_sync():
    asyncio.run(clear_month_expense())

