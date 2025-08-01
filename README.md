# Structured Prompt Generator (Streamlit)

A modern, user-friendly AI prompt generator built with Python Streamlit. This tool supports both English and Chinese, allows dynamic addition/removal of multiple Actions, and provides real-time preview, copy, and download of standardized prompts.

## 🚀 Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Launch the app:
   ```bash
   streamlit run app.py
   ```

## 🗂️ Project Structure
- `app.py`: Main Streamlit app and UI logic
- `utils.py`: Prompt generation logic
- `requirements.txt`: Python dependencies
- `README.md`: Documentation

## ✨ Features
- **Sectioned Input**: Fill in five key sections—Role, Task, Action, Context, Output
- **Dynamic Multi-Action**: Add or remove multiple actions; each action is rendered as an individual prompt step
- **Live Preview**: Instantly preview the generated prompt on the right panel
- **One-Click Copy & Download**: Easily copy or download the generated prompt
- **Reset Functionality**: Quickly clear all fields
- **Bilingual Support**: Switch between English and Chinese UI and prompt templates

## 🖥️ How to Use
1. Select your language (English/中文)
2. Fill in each field on the left; use "➕ Add Action" to add as many actions as you need
3. Instantly preview the structured prompt on the right; use copy or download as needed
4. Click "Reset" to clear all inputs

## 📝 Example Output
```
# <Role>
- You are an expert in {domain} with specialization in {specialization}.

# <Task>
- Your task is to {specific goal}.

## Reasoning
- Let's think step by step.

## Action
- [Search("1. research for the latest stock index")]
- [Search("2. research for the latest market trend")]
- [Search("3. ensure information correctness")]

## Observation
- Based on the action result to generate output.
...
```

---

This project is ideal for prompt engineering, workflow design, and defining AI agent tasks. Easily generate, preview, and export structured prompts with multiple actions and multilingual support.
