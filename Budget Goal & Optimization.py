income = 50000  # Assume
savings_goal = 15000
current_expense = df['Amount'].sum()

if income - current_expense < savings_goal:
    gap = savings_goal - (income - current_expense)

    print(f"You need to reduce ₹{gap} in expenses to reach your savings goal.")