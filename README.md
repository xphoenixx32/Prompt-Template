# Structured Prompt Generator (Streamlit)

一個基於 Python Streamlit 的結構化 AI 提示詞生成器，支援多語言（中/英），可動態新增多個 Action，並即時預覽、複製與下載標準化 Prompt。

## 🚀 快速開始

1. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```
2. 啟動應用：
   ```bash
   streamlit run app.py
   ```

## 🗂️ 主要檔案
- `app.py`：主程式，Streamlit 前端與互動邏輯
- `utils.py`：提示詞組裝邏輯
- `requirements.txt`：依賴套件列表
- `README.md`：本說明文件

## ✨ 主要功能
- **分區填寫**：分為 Role、Task、Action、Context、Output 五大區塊，逐步填寫
- **Action 支援多條目**：可動態新增/刪除多個 Action，每個行動會獨立顯示於 Prompt
- **即時預覽**：右側可即時預覽生成的標準化 Prompt
- **一鍵複製/下載**：支援一鍵複製與下載產生的 Prompt
- **重置功能**：快速清空所有欄位
- **多語言切換**：支援中英文介面與 Prompt 結構

## 🖥️ 操作說明
1. 選擇語言（English/中文）
2. 依序於左側填寫各欄位內容，Action 區塊可點「➕ Add Action」新增多個行動
3. 右側即時預覽標準化 Prompt，並可複製或下載
4. 點擊「Reset」可清空所有內容

## 📝 範例
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

This project provides a modern, user-friendly interface for generating structured AI prompts. Users can flexibly add multiple actions, preview, copy, and download the generated prompt in real time. Suitable for prompt engineering, workflow design, and AI agent task definition.
