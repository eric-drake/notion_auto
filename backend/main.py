from backend.notion_utils import get_expenses_for_month, write_report_to_notion,clear_month_expense_sync,add_expenses_to_month_expense_sync

if __name__ == "__main__":
    # Select the month dynamically
    import datetime
    now = datetime.datetime.now()
    year = now.year
    month = now.month

    print(f"📌 Generating report for {year}-{month:02d}...")

    # Get expenses for the selected month
    expenses = get_expenses_for_month(year, month)
    if not expenses:
        print("⚠️ No expenses found for the selected month. Please check your database.")
    else:
        print(f"✅ Found {len(expenses)} expenses for {year}-{month:02d}")

    clear_month_expense_sync()
    add_expenses_to_month_expense_sync(expenses)

    # Generate report text
    total_spent = sum(exp["amount"] for exp in expenses)
    report_text = f"Total Expense: ${total_spent}\nClick below to analyze data in Notion."

    # Write report with expenses as children
    write_report_to_notion(year, month, report_text, expenses)

    print("✅ Monthly Report Process Completed!")