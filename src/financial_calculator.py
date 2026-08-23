def calculate_total_expenses(expenses_dict):
    """Calculates total expenses."""
    return sum(expenses_dict.values())

def calculate_remaining_income(monthly_income, total_expenses):
    """Calculates remaining income."""
    return monthly_income - total_expenses

def calculate_savings_ratio(savings, monthly_income):
    """Calculates savings ratio as a percentage."""
    if monthly_income <= 0:
        return 0.0
    return (savings / monthly_income) * 100

def calculate_expense_ratio(total_expenses, monthly_income):
    """Calculates expense ratio as a percentage."""
    if monthly_income <= 0:
        # If income is 0 and expenses exist, it's effectively infinite.
        return 100.0 if total_expenses > 0 else 0.0
    return (total_expenses / monthly_income) * 100

def calculate_preliminary_score(monthly_income, total_expenses, savings, debt_payments):
    """Calculates a preliminary health score from 0-100."""
    if monthly_income <= 0:
        return 0

    score = 100
    
    # 1. Savings ratio penalty/bonus (target ~20%)
    savings_ratio = (savings / monthly_income) * 100
    if savings_ratio < 10:
        score -= 20
    elif savings_ratio < 20:
        score -= 10
    elif savings_ratio >= 30:
        score = min(100, score + 10)
        
    # 2. Expense ratio penalty (target < 80%)
    expense_ratio = (total_expenses / monthly_income) * 100
    if expense_ratio > 100:
        score -= 40
    elif expense_ratio > 90:
        score -= 30
    elif expense_ratio > 80:
        score -= 15
        
    # 3. Debt burden penalty (target < 30%)
    debt_ratio = (debt_payments / monthly_income) * 100
    if debt_ratio > 50:
        score -= 30
    elif debt_ratio > 30:
        score -= 15

    # 4. Remaining balance penalty
    remaining = monthly_income - total_expenses
    if remaining < 0:
        score -= 30
    elif remaining == 0:
        score -= 15

    return max(0, min(100, score))
