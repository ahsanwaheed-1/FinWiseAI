import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# As requested by user, use gpt-5-nano
MODEL_NAME = "gpt-5-nano"

FINANCIAL_GOALS = [
    "Save money",
    "Emergency fund",
    "Pay off debt",
    "Vacation",
    "Start a business",
    "Improve budgeting"
]

CURRENCIES = {
    "USD": "$",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "INR": "₹",
    "AUD": "A$",
    "CAD": "C$"
}

EXPENSE_CATEGORIES = [
    "Housing / Rent",
    "Food",
    "Transportation",
    "Utilities",
    "Education",
    "Healthcare",
    "Entertainment",
    "Loan / Debt",
    "Other"
]
