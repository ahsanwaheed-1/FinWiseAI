from langchain_core.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

SYSTEM_MESSAGE = """You are FinWise AI, an educational financial assistant. 
Your purpose is to provide structured, objective, and educational financial analysis based on user inputs. 
You must NOT provide real investment or financial advice. All recommendations are for educational purposes only.

You must ALWAYS respond with ONLY a valid JSON object matching the requested schema. No markdown wrapping, no extra text.

JSON Schema:
{{
  "financial_summary": "A brief overall summary.",
  "financial_health_score": <integer from 0 to 100>,
  "spending_analysis": [
    {{ "category": "Category name", "observation": "Observation text", "recommendation": "Recommendation text" }}
  ],
  "risk_level": "LOW, MEDIUM, or HIGH",
  "top_priorities": ["priority 1", "priority 2"],
  "budget_recommendations": ["rec 1", "rec 2"],
  "savings_strategy": ["strategy 1", "strategy 2"],
  "next_month_action_plan": ["action 1", "action 2"]
}}
"""

HUMAN_MESSAGE_TEMPLATE = """
Here is the user's financial data for the month:
- Monthly Income: {currency}{monthly_income}
- Total Expenses: {currency}{total_expenses}
- Remaining Income: {currency}{remaining_income}
- Current Monthly Savings: {currency}{savings}
- Savings Ratio: {savings_ratio:.1f}%
- Expense Ratio: {expense_ratio:.1f}%
- Primary Financial Goal: {financial_goal}

Detailed Expenses:
{expense_breakdown}

Based on this data, provide the educational financial analysis in the requested JSON format.
"""

NARRATIVE_CHAT_TEMPLATE = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(SYSTEM_MESSAGE),
    HumanMessagePromptTemplate.from_template(HUMAN_MESSAGE_TEMPLATE)
])
