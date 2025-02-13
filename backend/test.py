import os
import requests
from dotenv import load_dotenv
from notion_utils import get_expenses_for_month, add_expenses_to_month_expense_sync, clear_month_database_sync, get_categories, get_accounts, get_imcome_for_month, add_incomes_to_month_income_sync

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
EXPENSES_DB_ID = os.getenv("EXPENSES_DB_ID")
CATEGORIES_DB_ID = os.getenv("CATEGORIES_DB_ID")
MONTHLY_REPORTS_DB_ID = os.getenv("MONTHLY_REPORTS_DB_ID")
SUBSCRIPTIONS_DB_ID = os.getenv("SUBSCRIPTIONS_DB_ID")
MONTH_EXPENSE_DB_ID = os.getenv("MONTH_EXPENSE_DB_ID")
MONTH_INCOME_DB_ID = os.getenv("MONTH_INCOME_DB_ID")
ACCOUNTS_DB_ID = os.getenv("ACCOUNTS_DB_ID")

def test():
    year = 2025  # Replace with the desired year for testing
    month = 2 # Replace with the desired month for testing

    print(f"📌 Testing report for {year}-{month:02d}...")

    #fetch categories first, as the list need to be used later
    category_list = get_categories()
    #Fetch accounts 
    account_list = get_accounts()
    # Fetch only relevant expenses
    expenses = get_expenses_for_month(year, month, category_list)
    if not expenses:
        print("⚠️ No expenses found for the selected month. Please check your database.")
    else:
        print(f"✅ Found {len(expenses)} expenses for {year}-{month:02d}")

    clear_month_database_sync(MONTH_EXPENSE_DB_ID)
    add_expenses_to_month_expense_sync(expenses)

    
    income = get_imcome_for_month(year, month, account_list)
    
    if not income:
        print("⚠️ No Income found for the selected month. Please check your database.")
    else:
        print(f"✅ Found {len(income)} Income for {year}-{month:02d}")
    clear_month_database_sync(MONTH_INCOME_DB_ID)
    add_incomes_to_month_income_sync(income)

    
    print("✅ Test Completed! Check Notion for the generated report.")


if __name__ == "__main__":
    test()