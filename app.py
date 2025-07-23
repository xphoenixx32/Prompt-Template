import streamlit as st
from utils import generate_prompt
import io
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Structured Prompt Generator", layout="wide")
st.page_icon = "🎩"

# Define fields and sections
FIELDS_I18N = {
    "en": [
        {"key": "domain", 
        "title": "Domain", 
        "placeholder": "e.g. digital marketing, machine learning, financial planning, software development...", 
        "description": "Define the main professional domain.", 
        "section": "Role"},
        {"key": "specialization", 
        "title": "Specialization", 
        "placeholder": "e.g. brand strategy and social media, deep learning and NLP, investment analysis, full-stack web development...", 
        "description": "Define the specific area of expertise.", 
        "section": "Role"},
        {"key": "specificGoal", 
        "title": "Specific Goal", 
        "placeholder": "e.g. create a comprehensive social media marketing strategy for a tech startup, analyze customer behavior patterns from sales data...", 
        "description": "Describe the concrete goal clearly.", 
        "section": "Task"},
        {"key": "action", 
        "title": "Action", 
        "placeholder": "e.g. market research for social media trends, customer segmentation analysis, competitive analysis...", 
        "description": "Define the specific action required.", 
        "section": "Action"},
        {"key": "details", 
        "title": "Context Details", 
        "placeholder": "e.g. Target audience: young professionals aged 25-35, Budget: $50k monthly, Industry: B2B SaaS...", 
        "description": "Provide background info and key details.", 
        "section": "Context"},
        {"key": "constraints", 
        "title": "Constraints", 
        "placeholder": "e.g. Must comply with GDPR regulations, Limited to organic social media only, No budget for paid advertising...", 
        "description": "Specify constraints and requirements.", 
        "section": "Context"},
        {"key": "format", 
        "title": "Output Format", 
        "placeholder": "e.g. markdown, JSON, PDF report, Excel spreadsheet...", 
        "description": "Specify output file format.", 
        "section": "Output"},
        {"key": "structure", 
        "title": "Structure", 
        "placeholder": "e.g. {title, executive_summary, analysis, recommendations, timeline}, {headers: [], data: [], charts: []}...", 
        "description": "Define output structure.", 
        "section": "Output"},
        {"key": "unwantedResult", 
        "title": "Unwanted Result", 
        "placeholder": "e.g. provide generic advice without specific data, include unverified claims, exceed 2000 words...", 
        "description": "Clearly state unwanted results.", 
        "section": "Output"}
    ],
    "zh": [
        {"key": "domain", 
        "title": "領域", 
        "placeholder": "例如：數位行銷、機器學習、財務規劃、軟體開發...", 
        "description": "定義主要專業領域", 
        "section": "角色"},
        {"key": "specialization", 
        "title": "專精項目", 
        "placeholder": "例如：品牌策略與社群媒體、深度學習與 NLP、投資分析、全端網頁開發...", 
        "description": "定義具體專精項目", 
        "section": "角色"},
        {"key": "specificGoal", 
        "title": "具體目標", 
        "placeholder": "例如：為新創科技公司制定完整社群行銷策略、分析銷售數據中的顧客行為模式...", 
        "description": "明確描述具體目標", 
        "section": "任務"},
        {"key": "action", 
        "title": "行動", 
        "placeholder": "例如：社群趨勢市場調查、顧客分群分析、競品分析...", 
        "description": "定義需要執行的具體行動", 
        "section": "行動"},
        {"key": "details", 
        "title": "背景細節", 
        "placeholder": "例如：目標族群：25-35 歲年輕專業人士、預算：每月五萬美金、產業：B2B SaaS...", 
        "description": "提供背景資訊和重要細節", 
        "section": "背景"},
        {"key": "constraints", 
        "title": "限制條件", 
        "placeholder": "例如：必須符合 GDPR 規範、僅限自然社群流量、無付費廣告預算...", 
        "description": "說明限制條件和約束", 
        "section": "背景"},
        {"key": "format", 
        "title": "輸出格式", 
        "placeholder": "例如：markdown、JSON、PDF 報告、Excel 試算表...", 
        "description": "指定輸出檔案格式", 
        "section": "輸出"},
        {"key": "structure", 
        "title": "結構", 
        "placeholder": "例如：{title, executive_summary, analysis, recommendations, timeline}、{headers: [], data: [], charts: []}...", 
        "description": "定義輸出結構", 
        "section": "輸出"},
        {"key": "unwantedResult", 
        "title": "避免結果", 
        "placeholder": "例如：僅給出泛泛建議、包含未經查證的說法、超過 2000 字...", 
        "description": "明確不希望出現的結果", 
        "section": "輸出"}
    ]
}

SECTIONS_I18N = {
    "en": ["Role", "Task", "Action", "Context", "Output"],
    "zh": ["角色", "任務", "行動", "背景", "輸出"]
}

APP_I18N = {
    "en": {
        "title": "Structured Prompt Generator",
        "subtitle": "A standardized prompt generator.",
        "fill_header": "Fill in Parameters",
        "preview_header": "Preview",
        "show_preview": "Show/Hide Preview",
        "copy_btn": "Copy Prompt",
        "copied_msg": "Copied! (Please manually copy the content above)",
        "download_btn": "Download File",
        "reset_btn": "Reset",
        "structure_explanation": """
        ### 📋 Structure Explanation\n
        - **Role:** Define the professional domain and specialization\n
        - **Task:** Clearly describe the specific task to accomplish\n
        - **Action:** Specify the required search or analysis actions\n
        - **Context:** Provide background information and constraints\n
        - **Output:** Specify output format and unwanted results\n
        ---\n
        ### 💡 Usage Tips\n
        # - All fields are optional\n
        # - It is recommended to fill at least Domain and Task\n
        # - Unfilled fields will keep `{placeholder}` format\n
        # - Domain and Specialization are now filled separately\n
        # """
    },
    "zh": {
        "title": "結構化提示詞生成器",
        "subtitle": "基於標準化架構的提示詞生成器",
        "fill_header": "填入參數",
        "preview_header": "生成預覽",
        "show_preview": "顯示/隱藏 預覽",
        "copy_btn": "複製 Prompt",
        "copied_msg": "已複製!（請手動複製上方內容）",
        "download_btn": "下載檔案",
        "reset_btn": "重置",
        "structure_explanation": """### 📋 架構說明\n
        - **角色:** 定義專業領域和專精項目\n
        - **任務:** 明確說明要完成的具體任務\n
        - **行動:** 指定需要執行的搜尋或分析動作\n
        - **背景:** 提供背景資訊和限制條件\n
        - **輸出:** 規範輸出格式和避免的結果\n
        ---\n
        ### 💡 使用提示\n
        - 所有欄位都是選填\n
        - 建議至少填寫領域和目標\n
        - 未填寫的欄位會保持 `{placeholder}` 格式\n
        - 領域和專精項目現在分開填寫\n
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
    "en": ["Intro", "Let's Work"],
    "zh": ["介紹說明", "開始製作"]
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
            {"icon": "🧑‍💼", "title": "Role", "desc": "Define the professional domain and specialization."},
            {"icon": "🎯", "title": "Task", "desc": "Describe the specific task to accomplish."},
            {"icon": "🔍", "title": "Action", "desc": "Specify required search or analysis actions."},
            {"icon": "📚", "title": "Context", "desc": "Provide background info and constraints."},
            {"icon": "📤", "title": "Output", "desc": "Specify output format and unwanted results."},
        ],
        "zh": [
            {"icon": "🧑‍💼", "title": "角色", "desc": "定義專業領域和專精項目"},
            {"icon": "🎯", "title": "任務", "desc": "明確說明要完成的具體任務"},
            {"icon": "🔍", "title": "行動", "desc": "指定需要執行的搜尋或分析動作"},
            {"icon": "📚", "title": "背景", "desc": "提供背景資訊和限制條件"},
            {"icon": "📤", "title": "輸出", "desc": "規範輸出格式和避免的結果"},
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
            with st.expander(f"{section}", expanded=True):
                for field in [f for f in FIELDS if f["section"] == section]:
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
            st.code(prompt, language="markdown")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(ui["copy_btn"]):
                st.session_state["copied"] = True
                st.write(ui["copied_msg"])
        with col2:
            buf = io.StringIO()
            buf.write(prompt)
            st.download_button(
                label=ui["download_btn"],
                data=buf.getvalue(),
                file_name=f"generated_prompt_{st.session_state['lang']}.txt",
                mime="text/plain"
            )
        with col3:
            if st.button(ui["reset_btn"]):
                st.session_state["form_data"] = {field["key"]: "" for field in FIELDS}
                st.experimental_rerun()

