import streamlit as st
import ast
import textwrap
import subprocess

# Set page config at the very beginning
st.set_page_config(page_title="Code Error Detector", page_icon="🐍", layout="centered")

# Custom CSS to center title
st.markdown("""
    <style>
        .title {
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

def check_python_syntax(code):
    try:
        ast.parse(code)
        return "✅ No syntax errors found! Your Python code looks great!", None
    except SyntaxError as e:
        error_message = f"❌ Syntax Error: {e.msg}\\n📍 Line {e.lineno}, Column {e.offset}"
        return error_message, code

def check_javascript_syntax(code):
    try:
        process = subprocess.run(["node", "-e", code], capture_output=True, text=True)
        if process.returncode == 0:
            return "✅ No syntax errors found! Your JavaScript code looks great!", None
        else:
            return f"❌ JavaScript Error: {process.stderr}", code
    except Exception as e:
        return f"❌ JavaScript Execution Error: {str(e)}", code

# Streamlit UI
st.markdown("<h1 class='title'>🧑‍💻 AI-Powered Code Error Detector</h1>", unsafe_allow_html=True)
st.write("Check your Python & JavaScript code for syntax errors instantly! Just paste your code below and get instant feedback. 🚀")

# Code input
code = st.text_area("✍️ Paste your code here:", height=200)
code_type = st.radio("Select Code Type:", ("Python", "JavaScript"))

if st.button("🔍 Check for Errors"):
    if code.strip():
        if code_type == "Python":
            result, error_code = check_python_syntax(code)
        else:
            result, error_code = check_javascript_syntax(code)
        
        st.code(textwrap.dedent(result), language="python" if code_type == "Python" else "javascript")
        
        if error_code:
            st.subheader("⚠️ Error in Your Code:")
            st.code(error_code, language="python" if code_type == "Python" else "javascript")
    else:
        st.warning("⚠️ Please enter some code to check!")

# Instructions
st.markdown("""
## 📜 How to Use?
1. Paste your Python or JavaScript code in the text area above.
2. Select the **code type** (Python or JavaScript).
3. Click on **'🔍 Check for Errors'**.
4. If there are no syntax errors, you'll see a ✅ success message.
5. If there's a syntax error, it'll show the exact issue with the **line number** and **column** for Python.
6. The problematic code will also be displayed for debugging.

⚠️ **Requirements:** ⚠️
- **Python Checking:** This tool requires **Python 3.x** with the `ast` module (built-in).
- **JavaScript Checking:** Requires **Node.js** installed on your system.
  - Download Node.js from: [https://nodejs.org](https://nodejs.org)

🚀 Happy Coding! 🐍💡
""")
