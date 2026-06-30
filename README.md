# 🧠 DevFlow — AI Code Review Assistant

An AI-powered code review tool that analyzes your code for bugs, security issues, and quality — then rewrites it and generates unit tests.

## What it does
- 🐛 Finds bugs and issues with line references
- ⭐ Rates code quality out of 10
- 📖 Explains what the code does in plain English
- 🔒 Scans for security vulnerabilities (SQL injection, hardcoded secrets, etc.)
- 🔧 Rewrites your code in a production-ready refactored version
- 🧪 Auto-generates unit tests
- 🌐 Supports Python, TypeScript, JavaScript, C#, Java

## Tech Stack
- Python
- Streamlit
- Groq API (Llama 3.3 70B)
- python-dotenv

## How to run
1. Clone the repo
2. Run `pip install streamlit groq python-dotenv`
3. Add your Groq API key to a `.env` file:
4. Run `streamlit run app.py`

## Why 70B?
This project uses `llama-3.3-70b-versatile` instead of the smaller 8B model
because code review requires deeper reasoning and more accurate analysis.
