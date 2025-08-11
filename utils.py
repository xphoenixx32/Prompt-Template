def generate_prompt(form_data, lang="en"):
    """
    Generate the structured AI prompt based on input fields.
    Args:
        form_data (dict): Dictionary with keys: domain, specialization, specificGoal, action, details, constraints, format, structure, unwantedResult
        lang (str): 'en' for English, 'zh' for Chinese
    Returns:
        str: The generated prompt string.
    """
    if lang == "zh":
        # 行動區塊處理
        actions = form_data.get('action')
        zh_type_map = {
            "Search": "搜尋",
            "Lookup": "查找",
            "Browse": "瀏覽"
        }
        # Build Chinese prompt line-by-line to avoid indentation issues
        lines = []
        lines.append("# <角色>")
        lines.append(f"- 你是 {form_data.get('domain') or '{領域}'} 的專家，專精於 {form_data.get('specialization') or '{專精項目}'}。")
        lines.append("")
        lines.append("# <任務>")
        lines.append(f"- 你的任務是 {form_data.get('specificGoal') or '{具體目標}'}。")
        lines.append("")
        lines.append("# <情境>")
        lines.append("- 你需要的背景資訊：")
        lines.append(f"  - {form_data.get('details') or '{背景細節}'}")
        lines.append(f"  - {form_data.get('constraints') or '{限制條件}'}")
        lines.append("")
        lines.append("# <先推理再行動>")
        lines.append("## 推理")
        lines.append("- 讓我們一步一步思考。")
        lines.append("## 行動")
        # actions
        action_lines = []
        if isinstance(actions, list):
            for a in actions or []:
                val = (a or {}).get("value", "").strip()
                if val:
                    action_lines.append(f"- [{zh_type_map.get((a or {}).get('type'), (a or {}).get('type'))}(\"{val}\")]")
        elif isinstance(actions, str):
            for v in actions.split("\n"):
                v = v.strip()
                if v:
                    action_lines.append(f"- [搜尋(\"{v}\")]")
        if not action_lines:
            action_lines = ["- [搜尋(\"{行動}\")]"]
        lines.extend(action_lines)
        lines.append("## 觀察")
        lines.append("- 依據行動的結果產出答案。")
        lines.append("")
        lines.append("# <輸出格式>")
        if form_data.get('structure'):
            lines.append(f"- 請以 {form_data.get('format') or '{輸出格式}'} 格式，並依照下列結構：{form_data.get('structure')}")
        else:
            lines.append(f"- 請以 {form_data.get('format') or '{輸出格式}'} 格式，結構可自行決定。")
        lines.append(f"- 請避免 {form_data.get('unwantedResult') or '{避免結果}'}。")
        prompt = "\n".join(lines)
    else:
        actions = form_data.get('action')
        # Build English prompt line-by-line to avoid indentation issues
        lines = []
        lines.append("# <Role>")
        lines.append(f"- You are an expert in {form_data.get('domain') or '{domain}'} with specialization in {form_data.get('specialization') or '{specialization}'}.")
        lines.append("")
        lines.append("# <Task>")
        lines.append(f"- Your task is to {form_data.get('specificGoal') or '{specific goal}' }.")
        lines.append("")
        lines.append("# <Context>")
        lines.append("- Here is the context you need: ")
        lines.append(f"  - {form_data.get('details') or '{details}'}")
        lines.append(f"  - {form_data.get('constraints') or '{constraints}'}")
        lines.append("")
        lines.append("# <ReAct Framework: Reasoning & Action>")
        lines.append("## Reasoning")
        lines.append("- Let's think step by step.")
        lines.append("## Action")
        # actions
        action_lines = []
        if isinstance(actions, list):
            for a in actions or []:
                val = (a or {}).get("value", "").strip()
                if val:
                    action_lines.append(f"- [{(a or {}).get('type', 'Search')}(\"{val}\")]")
        elif isinstance(actions, str):
            for v in actions.split("\n"):
                v = v.strip()
                if v:
                    action_lines.append(f"- [Search(\"{v}\")]")
        if not action_lines:
            action_lines = ["- [Search(\"{action}\")]"]
        lines.extend(action_lines)
        lines.append("## Observation")
        lines.append("- Use the action results to produce the answer.")
        lines.append("")
        lines.append("# <Output Format>")
        if form_data.get('structure'):
            lines.append(f"- Return a {form_data.get('format') or '{format}'} file: follow this structure: {form_data.get('structure')}")
        else:
            lines.append(f"- Return a {form_data.get('format') or '{format}'} file (any structure is fine).")
        lines.append(f"- Don't {form_data.get('unwantedResult') or '{unwanted result}'}")
        prompt = "\n".join(lines)
    return prompt
