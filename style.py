# 文件名：style.py
import streamlit as st

def apply_common_style():
    # 1. 注入 CSS
    custom_css = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    [data-testid="stFileUploadDropzone"] > div > div { font-size: 0px !important; }
    [data-testid="stFileUploadDropzone"] > div > div::after {
        content: "📁 请将 Excel 文件拖拽到此处，或点击右侧按钮";
        font-size: 16px !important; color: #4A5568 !important; font-weight: 600 !important;
        display: block !important; margin-bottom: 5px !important;
    }
    [data-testid="stFileUploadDropzone"] button { font-size: 0px !important; }
    [data-testid="stFileUploadDropzone"] button::after {
        content: "选择文件"; font-size: 14px !important; display: block !important;
    }

    .stButton>button {
        border-radius: 8px !important; font-weight: bold !important;
        border: 1px solid #E2E8F0 !important; transition: all 0.3s ease !important;
    }
    .stButton>button:hover {
        border-color: #4C68FF !important; color: #4C68FF !important;
        box-shadow: 0 4px 12px rgba(76, 104, 255, 0.15) !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # 2. 注入统一的侧边栏
    with st.sidebar:
        st.markdown("## 📊 小白数据助手")
        st.caption("版本号: v1.0 | 为非技术人员打造")
        st.divider()
        st.info("💡 **小贴士**：\n可以在这里切换不同的数据处理工具哦！")