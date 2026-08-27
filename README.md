# FinWise AI

### DEPLOYED STREAMLIT LINK:

https://finwiseai-kvcns3kuzrqneympdvbu73.streamlit.app/

FinWise AI is an educational financial-assistant Streamlit web application. It takes user financial inputs, performs deterministic preliminary calculations in Python, and passes this data to an OpenAI LLM using LangChain. The LLM then provides a structured JSON analysis and recommendations which are streamed to the Streamlit frontend.

## Features

- **Streamlit UI**: Responsive form, tabs, sidebars, and metrics.
- **Python Deterministic Calculations**: Safely computes totals and ratios before invoking AI.
- **LangChain Integration**: Built with `ChatPromptTemplate` and `ChatOpenAI`.
- **Structured JSON Output**: Enforces strict JSON schema generation from the LLM.
- **Streaming Responses**: Real-time streaming generator for a natural typing effect.
- **Caching**: Configurable In-Memory and SQLite caching to reduce API costs and latency.
- **Bonus**: Expense Visualization (Plotly), PDF Reports (`fpdf2`), Multi-Currency, and Conversation History.

## Setup Instructions

1. **Clone/Navigate to the project directory:**
   ```bash
   cd FinWiseAI
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the environment:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Open `.env` and set your `OPENAI_API_KEY`.

## Run the Application

```bash
streamlit run app.py
```

## Python vs AI Separation
The application separates deterministic mathematics (like adding expenses or calculating percentages) from qualitative AI analysis. 
Calculations are handled in `src/financial_calculator.py` because LLMs can be unreliable with exact math. The exact calculations are then injected into the prompt context for the LLM to analyze the trends.

## Caching Strategy
This project utilizes LangChain's caching mechanisms (`InMemoryCache` and `SQLiteCache`). Caching prevents redundant API calls to OpenAI when identical inputs are submitted, saving both time and money. You can toggle the cache backend via the sidebar settings in the app.
