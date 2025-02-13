import os
import requests
from dotenv import load_dotenv
from notion_utils import get_expenses_for_month, add_expenses_to_month_expense_sync, clear_month_expense_sync, get_categories

def test():
    year = 2025  # Replace with the desired year for testing
    month = 2 # Replace with the desired month for testing

    print(f"📌 Testing report for {year}-{month:02d}...")

    #fetch categories first, as the list need to be used later
    category_list = get_categories()
    # Fetch only relevant expenses
    expenses = get_expenses_for_month(year, month, category_list)
    #expenses = get_all_expenses()
    
    if not expenses:
        print("⚠️ No expenses found for the selected month. Please check your database.")
    else:
        print(f"✅ Found {len(expenses)} expenses for {year}-{month:02d}")

    clear_month_expense_sync()
    add_expenses_to_month_expense_sync(expenses)

    print("✅ Test Completed! Check Notion for the generated report.")


if __name__ == "__main__":
    test()