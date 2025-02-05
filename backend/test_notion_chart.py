from notion_utils import get_expenses_for_month, write_report_to_notion, get_all_expenses
import datetime

def test_generate_monthly_report():
    """Test fetching expenses for a specific month and creating a Notion report"""
    year = 2025  # Replace with the desired year for testing
    month = 2  # Replace with the desired month for testing

    print(f"📌 Testing report for {year}-{month:02d}...")

    # Fetch only relevant expenses
    expenses = get_expenses_for_month(year, month)
    #expenses = get_all_expenses()
    
    if not expenses:
        print("⚠️ No expenses found for the selected month. Please check your database.")
    else:
        print(f"✅ Found {len(expenses)} expenses for {year}-{month:02d}")

    # Generate test report text
    total_spent = sum(exp["amount"] for exp in expenses) if expenses else 0
    report_text = f"Test Monthly Report\nTotal Expense: ${total_spent}\nClick below to analyze data in Notion."

    # Write test report
    write_report_to_notion(year, month, report_text, expenses)

    print("✅ Test Completed! Check Notion for the generated report.")

if __name__ == "__main__":
    test_generate_monthly_report()