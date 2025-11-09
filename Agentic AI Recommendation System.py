def recommend_changes(summary, savings_goal, income):
    total_expense = summary.sum()
    current_savings = income - total_expense
    required_cut = savings_goal - current_savings

    if required_cut <= 0:
        print("Goal achieved! You're on track 🎯")
        return

    print(f"You need to cut ₹{required_cut}. Suggestions:")
    high_spend = summary.sort_values(ascending = False)

    for cat, val in high_spend.items():
        reduce_amt = (val / total_expense) * required_cut
        print(f" - Reduce {cat} by ₹{int(reduce_amt)}")