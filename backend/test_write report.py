import os
import requests
from dotenv import load_dotenv
from notion_utils import write_report_to_notion, get_expenses_for_month, get_categories, get_subscriptions
from datetime import date
from monthly_report_generator import generate_monthly_summary

load_dotenv()
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
EXPENSES_DB_ID = os.getenv("EXPENSES_DB_ID")
CATEGORIES_DB_ID = os.getenv("CATEGORIES_DB_ID")
MONTHLY_REPORTS_DB_ID = os.getenv("MONTHLY_REPORTS_DB_ID")
SUBSCRIPTIONS_DB_ID = os.getenv("SUBSCRIPTIONS_DB_ID")
MONTH_EXPENSE_DB_ID = os.getenv("MONTH_EXPENSE_DB_ID")
MONTH_INCOME_DB_ID = os.getenv("MONTH_INCOME_DB_ID")
ACCOUNTS_DB_ID = os.getenv("ACCOUNTS_DB_ID")

def test_report():
    today = date.today()
    categories = get_categories()
    expenses = get_expenses_for_month(today.year, today.month, categories)
    subscriptions = get_subscriptions()
    expenses,total_expense, total_budget, category_percentages, report_lines = generate_monthly_summary(categories, expenses, subscriptions)
    write_report_to_notion(today.year, today.month, report_lines, expenses, total_expense, total_budget, category_percentages,today)
    print("✅ Test Completed! Check Notion for the generated report.")


if __name__ == "__main__":
    test_report()