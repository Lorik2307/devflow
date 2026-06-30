import streamlit as st
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

st.set_page_config(page_title="DevFlow 🧠", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .main { padding: 2rem; }
    .stTextArea textarea { font-family: 'Courier New', monospace; font-size: 14px; }
    .metric-card { background: #1e1e2e; border-radius: 10px; padding: 1rem; margin: 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

st.title("🧠 DevFlow — AI Code Review Assistant")
st.write("Paste your code. Get a full professional review in seconds.")

col1, col2 = st.columns([1, 1])

with col1:
    language = st.selectbox("Language", ["Python", "TypeScript", "JavaScript", "C#", "Java", "Other"])
    code = st.text_area("📝 Paste your code here", height=400, placeholder="def my_function():\n    pass")

with col2:
    st.markdown("### ⚙️ Review Options")
    check_bugs = st.checkbox("🐛 Find Bugs & Issues", value=True)
    check_quality = st.checkbox("⭐ Rate Code Quality", value=True)
    check_refactor = st.checkbox("🔧 Suggest Refactoring", value=True)
    check_explain = st.checkbox("📖 Explain What It Does", value=True)
    check_tests = st.checkbox("🧪 Generate Unit Tests", value=True)
    check_security = st.checkbox("🔒 Security Analysis", value=True)

    st.markdown("---")
    st.markdown("### 📊 What you'll get:")
    st.markdown("- Overall quality score (0-10)")
    st.markdown("- Line-by-line issue detection")
    st.markdown("- Refactored version of your code")
    st.markdown("- Auto-generated unit tests")
    st.markdown("- Security vulnerability scan")

def review_code(code, language, options):
    sections = []
    
    if options["bugs"]:
        sections.append("BUGS: List every bug, error, or potential issue. Include line numbers if possible. If none, say 'No bugs found.'")
    if options["quality"]:
        sections.append("QUALITY_SCORE: Rate the code 0-10 and explain why in 2 sentences.")
    if options["explain"]:
        sections.append("EXPLANATION: Explain what this code does in simple plain English, 3-5 sentences.")
    if options["security"]:
        sections.append("SECURITY: List any security vulnerabilities (SQL injection, hardcoded secrets, unsafe inputs etc). If none, say 'No security issues found.'")
    if options["refactor"]:
        sections.append("REFACTORED_CODE: Rewrite the code with all improvements applied. Make it production-ready.")
    if options["tests"]:
        sections.append(f"UNIT_TESTS: Write comprehensive unit tests for this code in {language}.")

    prompt = f"""You are a senior software engineer doing a professional code review.
    
Review this {language} code and respond with EXACTLY these sections in order:
{chr(10).join(f'{i+1}. {s}' for i, s in enumerate(sections))}

Use these exact headers: BUGS:, QUALITY_SCORE:, EXPLANATION:, SECURITY:, REFACTORED_CODE:, UNIT_TESTS:

Code to review:
```{language.lower()}
{code}
```

Be specific, professional, and thorough. This is a real code review."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=3000,
        temperature=0.3
    )
    return response.choices[0].message.content

def parse_and_display(review_text, options):
    
    if "QUALITY_SCORE:" in review_text:
        score_section = review_text.split("QUALITY_SCORE:")[1].split("\n")[0].strip()
        words = score_section.split()
        score_num = ''.join(filter(lambda x: x.isdigit() or x == '.', words[0])) if words else "0"
        try:
            score = float(score_num) if score_num else 0
            if score >= 8:
                st.success(f"## ⭐ Quality Score: {score}/10 — Excellent!")
            elif score >= 6:
                st.warning(f"## ⭐ Quality Score: {score}/10 — Good, some improvements needed")
            elif score >= 4:
                st.warning(f"## ⭐ Quality Score: {score}/10 — Needs work")
            else:
                st.error(f"## ⭐ Quality Score: {score}/10 — Major issues found")
        except:
            st.info(f"## ⭐ Quality Score: {score_section}")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🐛 Bugs", "📖 Explanation", "🔒 Security", "🔧 Refactored Code", "🧪 Unit Tests"])

    with tab1:
        if "BUGS:" in review_text:
            bugs = review_text.split("BUGS:")[1].split("QUALITY_SCORE:")[0].strip()
            st.markdown(bugs)

    with tab2:
        if "EXPLANATION:" in review_text:
            explanation = review_text.split("EXPLANATION:")[1].split("SECURITY:")[0].strip()
            st.markdown(explanation)

    with tab3:
        if "SECURITY:" in review_text:
            security = review_text.split("SECURITY:")[1].split("REFACTORED_CODE:")[0].strip()
            st.markdown(security)

    with tab4:
        if "REFACTORED_CODE:" in review_text:
            refactored = review_text.split("REFACTORED_CODE:")[1].split("UNIT_TESTS:")[0].strip()
            st.code(refactored, language=language.lower())

    with tab5:
        if "UNIT_TESTS:" in review_text:
            tests = review_text.split("UNIT_TESTS:")[1].strip()
            st.code(tests, language=language.lower())

if st.button("🚀 Run Code Review", type="primary") and code:
    options = {
        "bugs": check_bugs,
        "quality": check_quality,
        "refactor": check_refactor,
        "explain": check_explain,
        "tests": check_tests,
        "security": check_security
    }
    
    with st.spinner("🧠 Analyzing your code with AI..."):
        review = review_code(code, language, options)
    
    st.markdown("---")
    st.markdown("## 📊 Review Results")
    parse_and_display(review, options)
    
    with st.expander("📄 View Raw Review"):
        st.text(review)