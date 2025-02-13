from backend.notion_utils import get_expenses, get_categories, get_subscriptions


def generate_monthly_summary():
    """Processes expenses and generates a monthly summary"""
    expenses = get_expenses()
    categories = get_categories()
    subscription_expenses = get_subscriptions()

    # Convert categories into a dictionary for easy lookup
    category_budget_map = {c["category"]: c["budget"] for c in categories}

    # Calculate total spent per category
    category_expense_summary = {}
    total_expense = 0
    total_budget = sum(category_budget_map.values())

    for expense in expenses:
        category = expense["category"]
        amount = expense["amount"]
        total_expense += amount  # Add to total expenses

        if category in category_expense_summary:
            category_expense_summary[category] += amount
        else:
            category_expense_summary[category] = amount

    # Calculate usage percentage per category
    category_percentages = {
        category: (spent / category_budget_map.get(category, 1)) * 100
        for category, spent in category_expense_summary.items()
    }

    # Prepare a summary report text
    report_lines = [f"Total Expense: {total_expense} / Budget: {total_budget}"]
    for category, total_spent in category_expense_summary.items():
        budget = category_budget_map.get(category, 0)
        status = "Over Budget" if total_spent > budget else "Within Budget"
        percent_used = category_percentages[category]
        report_lines.append(f"Category: {category} | Spent: {total_spent} | Budget: {budget} | Used: {percent_used:.2f}% | Status: {status}")

    return total_expense, total_budget, category_percentages, "\n".join(report_lines)

