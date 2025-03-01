def generate_monthly_summary(category_list, expenses, subcription_list):
    """Processes expenses and generates a monthly summary"""
    NO_BUDGET_CATEGORY_LIST = ['Beauty','Commute','Investment','Rent', 'Utilities', 'Subscription']
    categories = category_list
    expenses = expenses
    subcription_list = subcription_list
    

    # Convert categories into a dictionary for easy lookup
    category_budget_map = {c["category"]: c["budget"] or 0 for c in categories}
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
    # Combine expenses for categories in NO_BUDGET_CATEGORY_LIST
    no_budget_total = sum(
        amount for category, amount in category_expense_summary.items() if category in NO_BUDGET_CATEGORY_LIST
    )
    # Remove individual no-budget categories from the summary
    for category in NO_BUDGET_CATEGORY_LIST:
        category_expense_summary.pop(category, None)
    # Add combined no-budget total to the summary
    category_expense_summary["Other"] = no_budget_total

    # Calculate usage percentage per category
    # Add subscription expenses to the budget
    

    category_percentages = {
        category: (spent / category_budget_map.get(category, 1)) * 100
        for category, spent in category_expense_summary.items()
    }

    # Calculate percentage for "Other" category
    other_budget_total = sum(category_budget_map.get(cat, 0) for cat in NO_BUDGET_CATEGORY_LIST)
    for subscription in subcription_list:
        if subscription['status'] == 'Active':
            other_budget_total += subscription['cost']

    category_budget_map["Other"] = other_budget_total
    

    category_percentages["Other"] = (no_budget_total / other_budget_total) * 100 if other_budget_total else 0

    # Prepare a summary report text
    report_lines = [f"Total Expense/Budget: {total_expense:.2f}/{total_budget:.2f}"]
    for category, total_spent in category_expense_summary.items():
        budget = category_budget_map.get(category, 0)
        status = "Over Budget" if total_spent > budget else "Within Budget"
        percent_used = category_percentages[category]
        report_lines.append(f"Category: {category} | Expense: {total_spent:.2f} | Budget: {budget:.2f}")
        report_lines.append(f"Used: {percent_used:.2f}% | Status: {status}")

    return expenses, total_expense, total_budget, category_percentages, "\n".join(report_lines)

