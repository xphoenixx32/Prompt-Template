# Structured Prompt Generator (Streamlit)

A modern, user-friendly AI prompt generator built with Python Streamlit. This tool supports English and Chinese, allows dynamic addition/removal of multiple Actions, and provides real-time preview, copy, and download of standardized prompts.

## 🚀 Quick Start

1. (Recommended) Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Launch the app:
   ```bash
   streamlit run app.py
   ```

## 🗂️ Project Structure
- `app.py`: Main Streamlit app and UI logic
- `utils.py`: Prompt generation logic
- `requirements.txt`: Python dependencies
- `README.md`: Documentation

## ✨ Features
- **Sectioned Input**: Fill in five key sections—Role, Task, Context, Action, Output
- **Dynamic Multi-Action**: Add or remove multiple actions; each action is rendered as an individual prompt step
- **Live Preview**: Instantly preview the generated prompt on the right panel
- **One-Click Copy & Download**: Copy via built-in code-block button plus an explicit "Copy" button; download as .txt
- **Reset Functionality**: Quickly clear all fields
- **Bilingual Support**: Switch between English and Chinese UI and prompt templates

## 🖥️ How to Use
1. Select your language (English/中文)
2. Fill in each field on the left; use "✅ Add Action" to add steps, and the trash icon to remove
3. Preview the structured prompt on the right; use the copy button or download
4. Click "Reset" to clear all inputs

## 📝 Example Output
```markdown
# <Role>
- You are an expert in {domain} with specialization in {specialization}.

# <Task>
- Your task is to {specific goal}.

# <Context>
- Here is the context you need:
  - {details}
  - {constraints}

# <ReAct Framework: Reasoning & Action>
## Reasoning
- Let's think step by step.
## Action
- [Search("latest market trend")]
- [Lookup("LLM basics")]
## Observation
- Use the action results to produce the answer.

# <Output Format>
- Return a {format} file (you can specify a structure).
- Don't {unwanted result}
```

---

This project is ideal for prompt engineering, workflow design, and defining AI agent tasks. Easily generate, preview, and export structured prompts with multiple actions and multilingual support.
