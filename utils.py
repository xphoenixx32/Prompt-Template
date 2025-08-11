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
        if isinstance(actions, list):
            if len(actions) == 0 or (len(actions) == 1 and (not actions[0] or not actions[0].get("value", "").strip())):
                actions_str = '- [搜尋("{行動}")]'  # placeholder
            else:
                actions_str = '\n'.join([
                    f'- [{zh_type_map.get(a.get("type"), a.get("type"))}("{a.get("value", "").strip()}")]'
                    for a in actions if a.get("value", "").strip()
                ])
        elif isinstance(actions, str):
            if actions.strip() == "":
                actions_str = '- [搜尋("{行動}")]'
            else:
                actions_str = '\n'.join([f'- [搜尋("{a.strip()}")]' for a in actions.split("\n") if a.strip()])
        else:
            actions_str = '- [搜尋("{行動}")]'

        prompt = f"""
            # <角色>
            - 你是 {form_data.get('domain') or '{領域}'} 的專家，專精於 {form_data.get('specialization') or '{專精項目}'}。

            # <任務>
            - 你的任務是 {form_data.get('specificGoal') or '{具體目標}'}。

            # <情境>
            - 你需要的背景資訊：
              - {form_data.get('details') or '{背景細節}'}
              - {form_data.get('constraints') or '{限制條件}'}

            # <先推理再行動>
            ## 推理
            - 讓我們一步一步思考。
            ## 行動
            {actions_str}
            ## 觀察
            - 依據行動的結果產出答案。

            # <輸出格式>
            - 請以 {form_data.get('format') or '{輸出格式}'} 格式，{('並依照下列結構：' + form_data.get('structure')) if form_data.get('structure') else '結構可自行決定。'}
            - 請避免 {form_data.get('unwantedResult') or '{避免結果}'}。"""
    else:
        actions = form_data.get('action')
        if isinstance(actions, list):
            if len(actions) == 0 or (len(actions) == 1 and (not actions[0] or not actions[0].get("value", "").strip())):
                actions_str = '- [Search("{action}")]'  # placeholder
            else:
                actions_str = '\n'.join([
                    f'- [{a.get("type", "Search")}("{a.get("value", "").strip()}")]'
                    for a in actions if a.get("value", "").strip()
                ])
        elif isinstance(actions, str):
            if actions.strip() == "":
                actions_str = '- [Search("{action}")]'
            else:
                actions_str = '\n'.join([f'- [Search("{a.strip()}")]' for a in actions.split("\n") if a.strip()])
        else:
            actions_str = '- [Search("{action}")]'

        prompt = f"""
            # <Role>
            - You are an expert in {form_data.get('domain') or '{domain}'} with specialization in {form_data.get('specialization') or '{specialization}'}.

            # <Task>
            - Your task is to {form_data.get('specificGoal') or '{specific goal}'}.

            # <Context>
            - Here is the context you need: 
              - {form_data.get('details') or '{details}'}
              - {form_data.get('constraints') or '{constraints}'}

            # <ReAct Framework: Reasoning & Action>
            ## Reasoning
            - Let's think step by step.
            ## Action
            {actions_str}
            ## Observation
            - Use the action results to produce the answer.

            # <Output Format>
            - Return a {form_data.get('format') or '{format}'} file{(': follow this structure: ' + form_data.get('structure')) if form_data.get('structure') else ' (any structure is fine).'}
            - Don't {form_data.get('unwantedResult') or '{unwanted result}'}"""
    return prompt
