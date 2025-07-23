# Structured Prompt Generator (Streamlit)

本專案將原本的 React/TSX Prompt Engineering Generator 轉換為 Python Streamlit 版本，提供一個簡單易用的 AI 提示詞生成器。

## 如何運行

1. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```
2. 啟動應用：
   ```bash
   streamlit run app.py
   ```

## 檔案結構
- `app.py`：主程式，Streamlit 前端
- `utils.py`：輔助函式
- `requirements.txt`：依賴套件
- `README.md`：本說明文件

## 功能
- 分區填寫：Role, Task, Action, Context, Output
- 動態生成標準化 AI Prompt
- 預覽、複製、下載、重置

---

This project is a Python Streamlit implementation of a structured prompt generator, migrated from a React/TSX architecture. It allows users to fill in various sections and generate a standardized AI prompt, with preview, copy, download, and reset options.
