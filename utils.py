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
        prompt = f"""# <角色>
- 你是 {form_data.get('domain') or '{領域}'} 的專家，專精於 {form_data.get('specialization') or '{專精項目}'}。

# <任務>
- 你的任務是 {form_data.get('specificGoal') or '{具體目標}'}。

## 推理
- 讓我們一步一步思考。

## 行動
- [搜尋(\"{form_data.get('action') or '{行動}'}\")]

## 觀察
- 根據行動結果產生輸出。

# <背景>
- 你需要的背景資訊：
  - {form_data.get('details') or '{背景細節}'}
  - {form_data.get('constraints') or '{限制條件}'}

# <輸出格式>
- 請以 {form_data.get('format') or '{輸出格式}'} 格式，並依照下列結構：{form_data.get('structure') or '{結構}'}
- 請避免 {form_data.get('unwantedResult') or '{避免結果}'}"""
    else:
        prompt = f"""# <Role>
- You are an expert in {form_data.get('domain') or '{domain}'} with specialization in {form_data.get('specialization') or '{specialization}'}.

# <Task>
- Your task is to {form_data.get('specificGoal') or '{specific goal}'}.

## Reasoning
- Let's think step by step.

## Action
- [Search(\"{form_data.get('action') or '{action}'}\")]

## Observation
- Based on the action result to generate output.

# <Context>
- Here is the context you need: 
  - {form_data.get('details') or '{details}'}
  - {form_data.get('constraints') or '{constraints}'}

# <Output Format>
- Return a {form_data.get('format') or '{format}'} file with the following structure: {form_data.get('structure') or '{...}'}
- Don't {form_data.get('unwantedResult') or '{unwanted result}'}"""
    return prompt
