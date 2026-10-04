import streamlit as st
import pandas as pd
import io

# 1. 页面基本配置
st.set_page_config(page_title="一键多表合并", layout="centered")

# 2. 盖上咱们做好的“软装”统一印章 (引用 style.py)
from style import apply_common_style

apply_common_style()

# ==========================================
# 3. 主页面内容 (卡片式精装排版 - 硬装升级)
# ==========================================
st.title("📂 一键多表合并")
st.markdown(
    "<p style='color:#718096; margin-bottom: 2rem;'>把格式相似的多个 Excel 拼成一个大表，支持合并所有 Sheet！</p>",
    unsafe_allow_html=True)

# --- 区域卡片 1：上传文件 ---
with st.container(border=True):
    st.subheader("第一步：导入多个数据表")
    # 这里的 label_visibility="collapsed" 是让它和首页完全一致的关键
    uploaded_files = st.file_uploader("", type=["xlsx", "xls"], accept_multiple_files=True,
                                      label_visibility="collapsed")

if uploaded_files:
    st.info(f"✅ 已接收 {len(uploaded_files)} 个文件。")

    # --- 区域卡片 2：设置合并规则 ---
    with st.container(border=True):
        st.subheader("第二步：设置合并规则")
        col1, col2 = st.columns(2)
        with col1:
            read_all_sheets = st.checkbox("合并每个文件里的所有 Sheet", value=False)
        with col2:
            add_source_col = st.checkbox("自动添加【来源信息】列", value=True)

    st.divider()

    # --- 区域卡片 3：开始合并与下载 ---
    # 注意这里的大按钮也换成了宽版 (use_container_width=True)
    if st.button("🚀 开始极速合并", type="primary", use_container_width=True):
        all_dataframes = []
        error_files = []

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, file in enumerate(uploaded_files):
            status_text.text(f"正在处理: {file.name} ...")
            try:
                if read_all_sheets:
                    sheets_dict = pd.read_excel(file, sheet_name=None)
                    for sheet_name, df in sheets_dict.items():
                        df = df.dropna(how='all')
                        if not df.empty:
                            if add_source_col:
                                df["_来源文件"] = file.name
                                df["_来源Sheet"] = sheet_name
                            all_dataframes.append(df)
                else:
                    df = pd.read_excel(file).dropna(how='all')
                    if not df.empty:
                        if add_source_col:
                            df["_来源文件"] = file.name
                        all_dataframes.append(df)
            except Exception:
                error_files.append(file.name)

            progress_bar.progress((i + 1) / len(uploaded_files))

        status_text.text("读取完成！正在进行底层数据拼装...")

        if not all_dataframes:
            st.error("❌ 没有提取到任何有效数据，请检查表格是否都是空的！")
        else:
            final_df = pd.concat(all_dataframes, ignore_index=True)

            with st.container(border=True):
                st.subheader("📊 合并结果")
                if error_files:
                    st.warning(f"⚠️ 以下文件读取失败被跳过：{', '.join(error_files)}")

                st.success(
                    f"🎉 大功告成！共提取了 {len(all_dataframes)} 个数据表，最终生成 {len(final_df)} 行数据的超级大表。")

                if len(final_df.columns) > 30:
                    st.info(
                        "💡 提示：合并后的列数较多。如果数据看起来错位了，通常是因为各个文件的【表头名字不一样】，系统已自动为您错开保留。")

                st.dataframe(final_df.head(100))

                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False, sheet_name='合并总表')

                st.download_button(
                    label="📥 立即下载合并后的 Excel",
                    data=output.getvalue(),
                    file_name="多表合并结果.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )