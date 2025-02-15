import os
from dotenv import load_dotenv
from notion_utils import write_report_to_notion, get_expenses_for_month, get_categories, get_subscriptions, clear_month_database_sync, add_expenses_to_month_expense_sync, get_imcome_for_month, add_incomes_to_month_income_sync, get_accounts
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

if __name__ == "__main__":
    # Select the month dynamically
    today = date.today()
    categories = get_categories()
    expenses = get_expenses_for_month(today.year, today.month, categories)
    subscriptions = get_subscriptions()

    print(f"📌 Generating report for {today.year}-{today.month:02d}...")

    expenses,total_expense, total_budget, category_percentages, report_lines = generate_monthly_summary(categories, expenses, subscriptions)
    write_report_to_notion(today.year, today.month, report_lines, expenses, total_expense, total_budget, category_percentages,today)
    print("✅ Monthly Report Completed! Check Notion for the generated report.")
    print("🚀 Updating monthly expense and income database")

    clear_month_database_sync(MONTH_EXPENSE_DB_ID)
    add_expenses_to_month_expense_sync(expenses)

    account_list = get_accounts()
    income = get_imcome_for_month(today.year, today.month, account_list)
    
    if not income:
        print("⚠️ No Income found for the selected month. Please check your database.")
    else:
        print(f"✅ Found {len(income)} Income for {today.year}-{today.month:02d}")
    clear_month_database_sync(MONTH_INCOME_DB_ID)
    add_incomes_to_month_income_sync(income)

    print("✅ Monthly Expense and Income Database Updated!")
