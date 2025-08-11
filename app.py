import streamlit as st
from utils import generate_prompt
import io
import json
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Structured Prompt Generator", layout="wide")
st.page_icon = "🎩"

# Action types and descriptions (multilingual)
ACTION_TYPES_I18N = {
    "en": [
        {
            "type": "Search",
            "label": "Search",
            "input_label": "Query",
            "placeholder": "e.g. latest AI news, market trend, competitor updates",
            "desc": "Find up-to-date info on the web."
        },
        {
            "type": "Lookup",
            "label": "Lookup",
            "input_label": "Topic",
            "placeholder": "e.g. LLM theory basics, Python list vs tuple, SWOT analysis",
            "desc": "Quickly learn a concept or topic."
        },
        {
            "type": "Browse",
            "label": "Browse",
            "input_label": "URL",
            "placeholder": "e.g. https://arxiv.org/abs/2307..., https://news.ycombinator.com/...",
            "desc": "Read a specific web page."
        }
    ],
    "zh": [
        {
            "type": "Search",
            "label": "搜尋",
            "input_label": "查詢內容",
            "placeholder": "例如：最新 AI 新聞、市場趨勢、競品資訊",
            "desc": "在網路上找最新資訊。"
        },
        {
            "type": "Lookup",
            "label": "查找",
            "input_label": "主題",
            "placeholder": "例如：LLM 基本觀念、Python list 與 tuple 差異、SWOT 分析",
            "desc": "快速了解一個概念或主題。"
        },
        {
            "type": "Browse",
            "label": "瀏覽",
            "input_label": "網址",
            "placeholder": "例如：https://arxiv.org/abs/2307...、https://news.ycombinator.com/...",
            "desc": "閱讀指定的網頁內容。"
        }
    ]
}

# Define fields and sections
FIELDS_I18N = {
    "en": [
        {"key": "domain", 
        "title": "Domain", 
        "placeholder": "e.g. digital marketing, machine learning, financial planning, software development...", 
        "description": "The general field you are working in.", 
        "section": "Role"},
        {"key": "specialization", 
        "title": "Specialization", 
        "placeholder": "e.g. brand strategy and social media, deep learning and NLP, investment analysis, full-stack web development...", 
        "description": "Your focus inside the domain.", 
        "section": "Role"},
        {"key": "specificGoal", 
        "title": "Specific Goal", 
        "placeholder": "e.g. create a comprehensive social media marketing strategy for a tech startup, analyze customer behavior patterns from sales data...", 
        "description": "What you want to achieve in one sentence.", 
        "section": "Task"},
        {"key": "action", 
        "title": "Action", 
        "placeholder": "e.g. market research for social media trends, customer segmentation analysis, competitive analysis...", 
        "description": "List the steps the assistant should take. Use \"Add Action\" for multiple steps.", 
        "section": "Action"},
        {"key": "details", 
        "title": "Context Details", 
        "placeholder": "e.g. Target audience: young professionals aged 25-35, Budget: $50k monthly, Industry: B2B SaaS...", 
        "description": "Key facts the assistant should know (audience, budget, industry...).", 
        "section": "Context"},
        {"key": "constraints", 
        "title": "Constraints", 
        "placeholder": "e.g. Must comply with GDPR regulations, Limited to organic social media only, No budget for paid advertising...", 
        "description": "Rules or limits to follow.", 
        "section": "Context"},
        {"key": "format", 
        "title": "Output Format", 
        "placeholder": "e.g. markdown, JSON, PDF report, Excel spreadsheet...", 
        "description": "Choose the file or text format for the answer.", 
        "section": "Output"},
        {"key": "structure", 
        "title": "Structure", 
        "placeholder": "e.g. {title, executive_summary, analysis, recommendations, timeline}, {headers: [], data: [], charts: []}...", 
        "description": "If you want a fixed structure, describe it here.", 
        "section": "Output"},
        {"key": "unwantedResult", 
        "title": "Unwanted Result", 
        "placeholder": "e.g. provide generic advice without specific data, include unverified claims, exceed 2000 words...", 
        "description": "What to avoid in the answer.", 
        "section": "Output"}
    ],
    "zh": [
        {"key": "domain", 
        "title": "領域", 
        "placeholder": "例如：數位行銷、機器學習、財務規劃、軟體開發...", 
        "description": "你正在處理的主要範疇。", 
        "section": "角色"},
        {"key": "specialization", 
        "title": "專精項目", 
        "placeholder": "例如：品牌策略與社群媒體、深度學習與 NLP、投資分析、全端網頁開發...", 
        "description": "在該領域中的專注方向。", 
        "section": "角色"},
        {"key": "specificGoal", 
        "title": "具體目標", 
        "placeholder": "例如：為新創科技公司制定完整社群行銷策略、分析銷售數據中的顧客行為模式...", 
        "description": "一句話說清楚你想達成什麼。", 
        "section": "任務"},
        {"key": "action", 
        "title": "行動", 
        "placeholder": "例如：社群趨勢市場調查、顧客分群分析、競品分析...", 
        "description": "列出助理要做的步驟。要多步驟可用「新增行動」。", 
        "section": "行動"},
        {"key": "details", 
        "title": "背景細節", 
        "placeholder": "例如：目標族群：25-35 歲年輕專業人士、預算：每月五萬美金、產業：B2B SaaS...", 
        "description": "助理需要知道的關鍵資訊（族群、預算、產業等）。", 
        "section": "情境"},
        {"key": "constraints", 
        "title": "限制條件", 
        "placeholder": "例如：必須符合一般資料保護規則的規範、僅限自然社群流量、無付費廣告預算...", 
        "description": "需要遵守的規則或限制。", 
        "section": "情境"},
        {"key": "format", 
        "title": "輸出格式", 
        "placeholder": "例如：markdown、JSON、PDF 報告、Excel 試算表...", 
        "description": "選擇輸出的檔案或文字格式。", 
        "section": "輸出"},
        {"key": "structure", 
        "title": "結構", 
        "placeholder": "例如：{title, executive_summary, analysis, recommendations, timeline}、{headers: [], data: [], charts: []}...", 
        "description": "若需要固定結構，請在此描述。", 
        "section": "輸出"},
        {"key": "unwantedResult", 
        "title": "避免結果", 
        "placeholder": "例如：僅給出泛泛建議、包含未經查證的說法、超過 2000 字...", 
        "description": "你不希望答案出現什麼。", 
        "section": "輸出"}
    ]
}

SECTIONS_I18N = {
    "en": ["① Role", "② Task", "③ Context", "④ Action", "⑤ Output"],
    "zh": ["① 角色", "② 任務", "③ 情境", "④ 行動", "⑤ 輸出"]
}

APP_I18N = {
    "en": {
        "title": "Structured Prompt Generator",
        "subtitle": "Create clear, consistent prompts step by step.",
        "fill_header": "Fill in Parameters",
        "preview_header": "Preview",
        "show_preview": "Show/Hide preview",
        "download_btn": "Download File",
        "reset_btn": "Reset",
        "structure_explanation": """
        ### 📋 Structure Explanation

        - **Role:** Your domain and specialization
        - **Task:** What you want to achieve
        - **Context:** Important background and constraints
        - **Action:** The steps to take (Search / Lookup / Browse)
        - **Output:** Format, structure, and what to avoid
        ---
        ### 💡 Usage Tips
        - All fields are optional
        - For best results, fill Domain and Task first
        - Empty fields will remain as `{placeholder}` in the preview
        - Domain and Specialization are filled separately
        """
    },
    "zh": {
        "title": "結構化提示詞生成器",
        "subtitle": "一步一步建立清楚、可迭代的提示詞",
        "fill_header": "填入參數",
        "preview_header": "生成預覽",
        "show_preview": "顯示/隱藏預覽",
        "download_btn": "下載檔案",
        "reset_btn": "重置",
        "structure_explanation": """### 📋 架構說明

        - **角色：** 你的領域與專精
        - **任務：** 想要達成的目標
        - **情境：** 重要背景與限制
        - **行動：** 要採取的步驟（搜尋／查找／瀏覽）
        - **輸出：** 格式、結構與需要避免的內容
        ---
        ### 💡 使用提示
        - 所有欄位皆為選填
        - 建議先填「領域」與「目標」
        - 未填寫的欄位會以 `{placeholder}` 顯示在預覽
        - 「領域」與「專精」分開填寫
        """
    }
}

# Language selection at the top
if "lang" not in st.session_state:
    st.session_state["lang"] = "en"

lang = option_menu(
    menu_title=None,
    options=["English", "中文"],
    icons=["sign-intersection-fill", "sign-merge-right-fill"],
    orientation="horizontal",
    default_index=0 if st.session_state["lang"] == "en" else 1,
)

st.session_state["lang"] = "en" if lang == "English" else "zh"

# Assign ui dictionary after language selection
ui = APP_I18N[st.session_state["lang"]]
FIELDS = FIELDS_I18N[st.session_state["lang"]]
SECTIONS = SECTIONS_I18N[st.session_state["lang"]]

st.markdown(f"""
<div style='text-align:center;'>
  <span style='display:block;font-size:1.6rem;font-weight:600;margin-bottom:0.2rem'>{ui['title']}</span>
  <span style='display:block;font-size:1.05rem;color:#888'>{ui['subtitle']}</span>
</div>
""", unsafe_allow_html=True)
st.divider()

if "form_data" not in st.session_state:
    st.session_state["form_data"] = {field["key"]: "" for field in FIELDS}

# Dynamic main section names based on language
MAIN_MENU = {
    "en": ["Intro", "Build Prompt"],
    "zh": ["概念說明", "開始建立提示詞"]
}
MAIN_ICONS = ["book", "pencil-fill"]
main_section = option_menu(
    menu_title=None,
    options=MAIN_MENU[st.session_state["lang"]],
    icons=MAIN_ICONS,
    # orientation="horizontal"
)

if main_section == MAIN_MENU[st.session_state["lang"]][0]:
    # Visually enhanced structure explanation (1x5 columns with icons)
    STRUCTURE_ITEMS = {
        "en": [
            {"icon": "🧑‍💼", "title": "Role", "desc": "Your domain and specialization."},
            {"icon": "🎯", "title": "Task", "desc": "What you want to achieve."},
            {"icon": "📚", "title": "Context", "desc": "Background details and rules."},
            {"icon": "🔍", "title": "Action", "desc": "Steps to search, learn, or browse."},
            {"icon": "📤", "title": "Output", "desc": "Format, structure, and avoid list."},
        ],
        "zh": [
            {"icon": "🧑‍💼", "title": "角色", "desc": "你的領域與專精。"},
            {"icon": "🎯", "title": "任務", "desc": "想達成的目標。"},
            {"icon": "📚", "title": "情境", "desc": "背景細節與規則。"},
            {"icon": "🔍", "title": "行動", "desc": "要搜尋、查找或瀏覽的步驟。"},
            {"icon": "📤", "title": "輸出", "desc": "格式、結構與避免清單。"},
        ]
    }
    st.divider()
    cols = st.columns(5)
    for i, item in enumerate(STRUCTURE_ITEMS[st.session_state["lang"]]):
        with cols[i]:
            st.markdown(f"<div style='text-align:center;font-size:2rem'>{item['icon']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;font-weight:bold;font-size:1.1rem'>{item['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align:center;color:#666;font-size:0.95rem'>{item['desc']}</div>", unsafe_allow_html=True)
    # Usage tips below
    st.markdown("---")
    USAGE_TIPS = {
        "en": """
        ### 💡 Usage Reminders\n
        - All fields are optional\n
        - It is recommended to fill at least Domain and Task\n
        - Unfilled fields will keep `{placeholder}` format\n
        """,
        "zh": """
        ### 💡 使用提醒\n
        - 所有欄位都是選填\n
        - 建議至少填寫領域和目標\n
        - 未填寫的欄位會保持 `{placeholder}` 格式\n
        """
    }
    st.markdown(USAGE_TIPS[st.session_state["lang"]])
else:
    # Show parameter input (left) and preview (right) together
    left, right = st.columns([1.5, 1], gap="large")
    with left:
        st.subheader(ui["fill_header"])
        for section in SECTIONS:
            # Normalize numbered labels like "① Role" -> "Role" or "① 角色" -> "角色"
            if isinstance(section, str) and " " in section and section[0] in "①②③④⑤⑥⑦⑧⑨⑩":
                base_section = section.split(" ", 1)[1]
            else:
                base_section = section
            with st.expander(f"{section}", expanded=False):
                if base_section == ("Action" if st.session_state["lang"] == "en" else "行動"):
                    action_types = ACTION_TYPES_I18N[st.session_state["lang"]]
                    # initialize as list of dict
                    if "action" not in st.session_state["form_data"] or not isinstance(st.session_state["form_data"]["action"], list):
                        st.session_state["form_data"]["action"] = [{"type": action_types[0]["type"], "value": ""}]
                    actions = st.session_state["form_data"]["action"]
                    n = len(actions)
                    for i in range(n):
                        c1, c2 = st.columns([8,1])
                        with c1:
                            # select Action type
                            action_type_label = (
                                f"no.{i+1} Action Type" if st.session_state["lang"] == "en" else f"第 {i+1} 個行動類型"
                            )
                            selected_type = st.selectbox(
                                label=action_type_label,
                                options=[t["type"] for t in action_types],
                                format_func=lambda x: next((t["label"] for t in action_types if t["type"] == x), x),
                                index=next((idx for idx, t in enumerate(action_types) if t["type"] == actions[i].get("type", action_types[0]["type"])), 0),
                                key=f"action_type_{i}"
                            )
                            actions[i]["type"] = selected_type
                            # get corresponding description and placeholder
                            type_config = next((t for t in action_types if t["type"] == selected_type), action_types[0])
                            actions[i]["value"] = st.text_area(
                                label=f"{type_config['input_label']}",
                                value=actions[i].get("value", ""),
                                placeholder=type_config["placeholder"],
                                help=type_config["desc"],
                                key=f"action_value_{i}"
                            )
                        with c2:
                            if n > 1:
                                remove_label = "🗑️ Remove" if st.session_state["lang"] == "en" else "🗑️ 刪除"
                                if st.button(remove_label, key=f"remove_action_{i}"):
                                    actions.pop(i)
                                    st.session_state["form_data"]["action"] = actions
                                    st.rerun()
                    add_label = "✅ Add Action" if st.session_state["lang"] == "en" else "✅ 新增行動"
                    if st.button(add_label, key="add_action"):
                        actions.append({"type": action_types[0]["type"], "value": ""})
                        st.session_state["form_data"]["action"] = actions
                        st.rerun()
                else:
                    for field in [f for f in FIELDS if f["section"] == base_section]:
                        if field["key"] == "action":
                            continue
                        if field["key"] == "structure":
                            # add selection toggle for optional structure
                            structure_toggle_label = "Specify Output Structure" if st.session_state["lang"] == "en" else "指定輸出結構"
                            if f"show_structure_{base_section}" not in st.session_state:
                                st.session_state[f"show_structure_{base_section}"] = False
                            show_structure = st.checkbox(structure_toggle_label, value=st.session_state[f"show_structure_{base_section}"], key=f"structure_toggle_{base_section}")
                            st.session_state[f"show_structure_{base_section}"] = show_structure
                            if show_structure:
                                st.session_state["form_data"][field["key"]] = st.text_area(
                                    label=field["title"],
                                    value=st.session_state["form_data"][field["key"]],
                                    placeholder=field["placeholder"],
                                    help=field["description"],
                                    key=field["key"]
                                )
                            else:
                                st.session_state["form_data"][field["key"]] = ""
                        else:
                            st.session_state["form_data"][field["key"]] = st.text_area(
                                label=field["title"],
                                value=st.session_state["form_data"][field["key"]],
                                placeholder=field["placeholder"],
                                help=field["description"],
                                key=field["key"]
                            )
    with right:
        st.subheader(ui["preview_header"])
        show_preview = st.checkbox(ui["show_preview"], value=True)
        prompt = generate_prompt(st.session_state["form_data"], lang=st.session_state["lang"])
        if show_preview:
            col1, col2 = st.columns(2)
            with col1:
                buf = io.StringIO()
                buf.write(prompt)
                st.download_button(
                    label=ui["download_btn"],
                    data=buf.getvalue(),
                    file_name=f"generated_prompt_{st.session_state['lang']}.txt",
                    mime="text/plain"
                )
            with col2:
                if st.button(ui["reset_btn"]):
                    st.session_state["form_data"] = {field["key"]: "" for field in FIELDS}
                    st.rerun()
            
            st.code(prompt, language="markdown")
            # Explicit copy-to-clipboard button to ensure availability across Streamlit versions/themes
            escaped = json.dumps(prompt)
            components.html(
                f"""
                <div style='margin-top:8px'>
                  <button id='copy-btn' style='padding:6px 10px;border:1px solid #ddd;border-radius:6px;background:#f7f7f7;cursor:pointer;'>📋 Copy</button>
                  <span id='copy-status' style='margin-left:8px;color:#888;'></span>
                </div>
                <script>
                  const btn = document.getElementById('copy-btn');
                  const statusEl = document.getElementById('copy-status');
                  const text = {escaped};
                  btn.addEventListener('click', async () => {{
                    try {{
                      await navigator.clipboard.writeText(text);
                      statusEl.textContent = 'Copied!';
                      setTimeout(() => statusEl.textContent = '', 1500);
                    }} catch(e) {{
                      statusEl.textContent = 'Copy failed';
                      setTimeout(() => statusEl.textContent = '', 1500);
                    }}
                  }});
                </script>
                """,
                height=0,
            )

