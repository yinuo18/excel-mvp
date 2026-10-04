import streamlit as st
import pandas as pd
import io

# 1. 页面基本配置
st.set_page_config(page_title="一键数据清洗", layout="centered")

# 2. 盖上咱们做好的“精装修”统一印章
from style import apply_common_style

apply_common_style()

# ==========================================
# 3. 主页面内容 (卡片式精装排版)
# ==========================================
st.title("🧼 一键数据清洗与体检")
st.markdown("<p style='color:#718096; margin-bottom: 2rem;'>告别肉眼找错！像做体检一样，自动去重、去空格、处理缺失值。</p>",
            unsafe_allow_html=True)

# --- 区域卡片 1：上传文件 ---
with st.container(border=True):
    st.subheader("第一步：导入数据")
    # 这里的 label_visibility="collapsed" 是关键，它能让样式和第一页完全保持一致！
    uploaded_file = st.file_uploader("", type=["xlsx", "xls"], label_visibility="collapsed")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # --- 区域卡片 2：数据体检报告 ---
    with st.container(border=True):
        st.subheader("第二步：数据体检报告")
        duplicate_count = df.duplicated().sum()
        missing_count = df.isna().sum().sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("总行数", f"{len(df)} 行")
        col2.metric("重复行数", f"{duplicate_count} 行", delta="建议清除" if duplicate_count > 0 else "完美",
                    delta_color="inverse")
        col3.metric("空白单元格", f"{missing_count} 个", delta="需留意" if missing_count > 0 else "完美",
                    delta_color="inverse")

    # --- 区域卡片 3：设置清洗规则 ---
    with st.container(border=True):
        st.subheader("第三步：设置一键清洗规则")

        clean_spaces = st.checkbox("✂️ 自动清除文字前后的多余空格", value=True)
        drop_duplicates = st.checkbox("🗑️ 删除完全重复的数据行", value=True)

        handle_na_option = st.selectbox(
            "🕳️ 遇到空白单元格怎么处理？",
            ["不处理 (保持原样)", "删除包含空值的整行", "把空值统一填成 '0'", "把空值统一填成 '未知'"]
        )

        st.divider()
        # 注意：这里也换成了和第一页一样的宽版大按钮
        if st.button("🚀 开始清洗", type="primary", use_container_width=True):
            cleaned_df = df.copy()

            if clean_spaces:
                for col in cleaned_df.select_dtypes(include=['object']).columns:
                    cleaned_df[col] = cleaned_df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

            if drop_duplicates:
                cleaned_df = cleaned_df.drop_duplicates()

            if handle_na_option == "删除包含空值的整行":
                cleaned_df = cleaned_df.dropna()
            elif handle_na_option == "把空值统一填成 '0'":
                cleaned_df = cleaned_df.fillna(0)
            elif handle_na_option == "把空值统一填成 '未知'":
                cleaned_df = cleaned_df.fillna("未知")

            st.success(f"🎉 清洗完成！最终保留了 {len(cleaned_df)} 行健康数据。")
            st.dataframe(cleaned_df.head(100))

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                cleaned_df.to_excel(writer, index=False, sheet_name='清洗后数据')

            st.download_button(
                label="📥 立即下载干净的 Excel",
                data=output.getvalue(),
                file_name="已清洗数据.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
