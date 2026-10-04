import streamlit as st
from markitdown import MarkItDown
import os
import zipfile
import io
# 1. 全局页面配置（必须在第一行）
st.set_page_config(
    page_title="文献解析舱 Pro | 专为深度科研打造",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. 注入现代化 SaaS 风格的 CSS 样式
st.markdown("""
<style>
    /* 全局背景色调优 */
    .stApp {
        background-color: #F8FAFC;
    }

    /* 隐藏默认的顶部线条和菜单，显得更像独立网站 */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 渐变色 Hero 横幅区 */
    .hero-banner {
        background: linear-gradient(135deg, #1E293B 0%, #3B82F6 100%);
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 3rem;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin-bottom: 1rem;
        letter-spacing: -1px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        font-weight: 400;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }

    /* 功能特性卡片 */
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 6px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        height: 100%;
        transition: transform 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.5rem;
    }
    .feature-desc {
        font-size: 0.9rem;
        color: #64748B;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# 3. 渲染高级横幅 (Hero Section)
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⚡ 智能文献解析舱 <span style="color:#60A5FA;">Pro</span></div>
    <div class="hero-subtitle">下一代科研预处理引擎 | 专为突破学术壁垒设计。将复杂的论文排版与实验数据，瞬间转化为大语言模型最爱的纯净结构化文本。</div>
</div>
""", unsafe_allow_html=True)

# 4. 渲染功能特性卡片（全学科痛点版）
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📚 文科专著与长文逻辑重构</div>
        <div class="feature-desc">解决大部头文献中页眉、页脚、繁杂脚注频繁截断正文的痛点。完美剥离双栏排版，让 AI 总结文史哲长篇论述不再“断章取义”。</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🔬 理工医学公式与复杂表格</div>
        <div class="feature-desc">硬核学术党福音。精准识别医学临床嵌套统计表，将复杂的数学推导、化学公式及实验台账，转化为大模型100%可读的结构化对齐文本。</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🌐 告别乱码：全格式语料转换</div>
        <div class="feature-desc">彻底告别直接喂 PDF 给 AI 导致的乱码灾难。支持将 Word 组会报告、PPT、Excel 实验数据源统一洗脱为纯净无噪的 Markdown 格式。</div>
    </div>
    """, unsafe_allow_html=True)

import streamlit as st
from markitdown import MarkItDown
import os
import zipfile
import io

# ... [保留前面的页面配置、CSS样式和特性卡片代码] ...

# 5. 核心交互区（批量处理版）
st.markdown("### 📥 开启批量解析工作流")
upload_col, empty_col = st.columns([2, 1])

with upload_col:
    # 关键修改 1：添加 accept_multiple_files=True，并将变量名改为复数 uploaded_files
    uploaded_files = st.file_uploader(
        "拖拽多个文件至此区域 (支持批量全选 PDF / XLSX / DOCX / PPTX / HTML)",
        type=["pdf", "docx", "pptx", "xlsx", "csv", "html"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

if uploaded_files:  # 当检测到文件列表不为空时
    st.markdown("---")

    # 在内存中创建一个 ZIP 压缩包，用来装所有转换后的 md 文件
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:

        # 遍历用户上传的每一个文件
        for file in uploaded_files:
            temp_path = file.name
            with open(temp_path, "wb") as f:
                f.write(file.getbuffer())

            with st.spinner(f"⏳ 正在解析: {file.name}..."):
                try:
                    md = MarkItDown()
                    result = md.convert(temp_path)
                    markdown_text = result.text_content

                    # 关键修改 2：将解析出的文本直接写入到 ZIP 包中
                    zip_file.writestr(f"Parsed_{file.name}.md", markdown_text)

                    # 在网页上为每个文件生成一个折叠面板，方便单独预览或下载
                    with st.expander(f"✅ {file.name} (解析成功)", expanded=False):
                        st.download_button(
                            label="⬇️ 单独下载",
                            data=markdown_text,
                            file_name=f"Parsed_{file.name}.md",
                            mime="text/markdown",
                            key=f"btn_{file.name}"  # 批量生成按钮时，key 必须唯一
                        )
                        st.text_area("文本预览：", markdown_text, height=150, key=f"text_{file.name}",
                                     label_visibility="collapsed")

                except Exception as e:
                    st.error(f"❌ 解析 {file.name} 失败: {e}")
                finally:
                    if os.path.exists(temp_path):
                        os.remove(temp_path)

    # 遍历结束后，在最醒目的位置提供一键打包下载按钮
    st.success(f"🎉 批量任务完成！共成功处理 {len(uploaded_files)} 个文件。")
    st.download_button(
        label="📦 一键打包下载全部 Markdown (.zip)",
        data=zip_buffer.getvalue(),
        file_name="批量解析结果_MarkItDown.zip",
        mime="application/zip",
        type="primary",
        use_container_width=True
    )