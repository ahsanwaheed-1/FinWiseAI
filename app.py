import streamlit as st
import pandas as pd
import plotly.express as px
from src.config import MODEL_NAME, FINANCIAL_GOALS, CURRENCIES, EXPENSE_CATEGORIES
from src.financial_calculator import (
    calculate_total_expenses, calculate_remaining_income,
    calculate_savings_ratio, calculate_expense_ratio,
    calculate_preliminary_score
)
from src.cache_manager import setup_cache
from src.chains import get_llm, stream_recommendations
from src.utils import parse_json_from_llm, generate_pdf_report

# Page Config
st.set_page_config(page_title="FinWise AI", page_icon="💸", layout="wide")

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "financial_inputs" not in st.session_state:
    st.session_state.financial_inputs = None

# Sidebar
with st.sidebar:
    st.title("💸 FinWise AI")
    st.markdown("Your educational financial assistant.")
    
    st.header("Settings")
    
    # Cache Selection
    cache_option = st.selectbox("Cache Backend", ["None", "In-Memory", "SQLite"], index=1)
    setup_cache(cache_option)
    
    # Currency
    currency_code = st.selectbox("Currency", list(CURRENCIES.keys()))
    currency_symbol = CURRENCIES[currency_code]
    
    # Theme toggle hint
    st.info("💡 Pro Tip: Toggle Dark/Light mode in the Streamlit Settings (top right menu).")
    
    # Reset Session
    if st.button("Reset Session"):
        st.session_state.messages = []
        st.session_state.analysis_result = None
        st.session_state.financial_inputs = None
        st.rerun()
        
    st.caption("Disclaimer: For educational purposes only. Not financial advice.")

# Main Layout
st.title("Financial Dashboard")

# Input Form
with st.expander("📝 Enter Your Financial Details", expanded=True):
    with st.form("financial_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Income & Savings")
            monthly_income = st.number_input("Monthly Income", min_value=0.0, step=100.0, value=None, placeholder="0.00")
            current_savings = st.number_input("Current Monthly Savings", min_value=0.0, step=50.0, value=None, placeholder="0.00")
            financial_goal = st.selectbox("Primary Financial Goal", FINANCIAL_GOALS)
            
        with col2:
            st.subheader("Expenses")
            expenses_dict = {}
            for cat in EXPENSE_CATEGORIES:
                expenses_dict[cat] = st.number_input(f"{cat}", min_value=0.0, step=50.0, value=None, placeholder="0.00")
                
        submit_button = st.form_submit_button("Analyze Finances")

if submit_button:
    # Handle empty fields
    monthly_income = monthly_income or 0.0
    current_savings = current_savings or 0.0
    for k in expenses_dict:
        expenses_dict[k] = expenses_dict[k] or 0.0
        
    # Runtime checks
    if current_savings > monthly_income:
        st.error("Error: Current Monthly Savings cannot be greater than Monthly Income.")
        st.stop()

    # Calculations
    total_expenses = calculate_total_expenses(expenses_dict)
    remaining_income = calculate_remaining_income(monthly_income, total_expenses)
    savings_ratio = calculate_savings_ratio(current_savings, monthly_income)
    expense_ratio = calculate_expense_ratio(total_expenses, monthly_income)
    
    # We use loan/debt specifically for preliminary score
    debt_payments = expenses_dict.get("Loan / Debt", 0.0)
    prelim_score = calculate_preliminary_score(monthly_income, total_expenses, current_savings, debt_payments)
    
    expense_breakdown = "\n".join([f"- {k}: {currency_symbol}{v}" for k, v in expenses_dict.items() if v > 0])
    
    inputs = {
        "monthly_income": monthly_income,
        "total_expenses": total_expenses,
        "remaining_income": remaining_income,
        "savings": current_savings,
        "savings_ratio": savings_ratio,
        "expense_ratio": expense_ratio,
        "financial_goal": financial_goal,
        "expense_breakdown": expense_breakdown,
        "currency": currency_symbol
    }
    
    st.session_state.financial_inputs = inputs
    
    # Build a message context for the UI history
    user_msg = f"Please analyze my finances. Income: {currency_symbol}{monthly_income}, Expenses: {currency_symbol}{total_expenses}."
    st.session_state.messages.append({"role": "user", "content": user_msg})
    
    llm = get_llm(model_name=MODEL_NAME)
    
    # We use a placeholder to show the streaming text
    with st.spinner("Analyzing..."):
        # We need to collect the full output to parse JSON
        full_response_text = ""
        placeholder = st.empty()
        
        # Stream from generator
        for chunk_text in stream_recommendations(llm, inputs):
            full_response_text += chunk_text
            placeholder.markdown(full_response_text + "▌")
            
        placeholder.empty() # clear raw JSON
        
        # Parse JSON
        parsed_data = parse_json_from_llm(full_response_text)
        st.session_state.analysis_result = parsed_data
        st.session_state.expenses_dict = expenses_dict
        
        st.session_state.messages.append({"role": "assistant", "content": "Analysis complete. See dashboard below."})

# Display Results if we have them
if st.session_state.analysis_result:
    inputs = st.session_state.financial_inputs
    data = st.session_state.analysis_result
    exp_dict = st.session_state.expenses_dict
    
    st.header("📊 Financial Overview")
    
    # Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Monthly Income", f"{currency_symbol}{inputs['monthly_income']:.2f}")
    m2.metric("Total Expenses", f"{currency_symbol}{inputs['total_expenses']:.2f}")
    m3.metric("Remaining Balance", f"{currency_symbol}{inputs['remaining_income']:.2f}")
    m4.metric("Current Savings", f"{currency_symbol}{inputs['savings']:.2f}")
    
    # Visualizations
    st.subheader("Expense Breakdown")
    # Filter out 0 expenses for chart
    chart_data = {k: v for k, v in exp_dict.items() if v > 0}
    if chart_data:
        df = pd.DataFrame(list(chart_data.items()), columns=['Category', 'Amount'])
        c1, c2 = st.columns(2)
        with c1:
            fig_pie = px.pie(df, values='Amount', names='Category', title='Expenses by Category (Pie)')
            st.plotly_chart(fig_pie, width="stretch")
        with c2:
            fig_bar = px.bar(df, x='Category', y='Amount', title='Expenses by Category (Bar)')
            st.plotly_chart(fig_bar, width="stretch")
    else:
        st.info("No expenses recorded.")
        
    st.header("🧠 AI Analysis & Insights")
    
    # Check for parse error
    if "error" in data:
        st.error(data["error"])
        st.code(data.get("raw_text", ""))
    else:
        score = data.get("financial_health_score", 0)
        st.progress(score / 100.0, text=f"Health Score: {score}/100")
        
        st.info(f"**Financial Summary:** {data.get('financial_summary', '')}")
        st.warning(f"**Risk Level:** {data.get('risk_level', 'Unknown')}")
        
        tab1, tab2, tab3, tab4 = st.tabs(["Spending Analysis", "Top Priorities", "Budget Recs", "Action Plan"])
        
        with tab1:
            for item in data.get("spending_analysis", []):
                with st.expander(f"{item.get('category', 'Category')}"):
                    st.write(f"**Observation:** {item.get('observation', '')}")
                    st.write(f"**Recommendation:** {item.get('recommendation', '')}")
                    
        with tab2:
            for p in data.get("top_priorities", []):
                st.markdown(f"- {p}")
                
        with tab3:
            for b in data.get("budget_recommendations", []):
                st.markdown(f"- {b}")
                
        with tab4:
            for a in data.get("next_month_action_plan", []):
                st.markdown(f"- {a}")

        # PDF Export
        st.subheader("📄 Export Report")
        pdf_bytes = generate_pdf_report(data, currency_symbol, inputs)
        if pdf_bytes:
            st.download_button(
                label="Download PDF Report",
                data=pdf_bytes,
                file_name="finwise_report.pdf",
                mime="application/pdf"
            )

# Display Conversation History
with st.expander("💬 Conversation History"):
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
