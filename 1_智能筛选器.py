import streamlit as st
import pandas as pd
import io

# 1. 页面基本配置（这里必须放在最第一行）
st.set_page_config(page_title="Excel 小白助手", page_icon="📊", layout="centered")

from style import apply_common_style
apply_common_style()
# ==========================================
# 4. 主页面内容
# ==========================================
st.title("🎯 智能数据筛选器")
st.markdown("<p style='color:#718096; margin-bottom: 2rem;'>无需复杂的公式，像点外卖一样点选条件，轻松找出目标数据。</p>",
            unsafe_allow_html=True)

# --- 区域卡片 1：上传文件 ---
with st.container(border=True):
    st.subheader("第一步：导入数据")
    uploaded_file = st.file_uploader("", type=["xlsx", "xls"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file).dropna(how='all')
        st.success(f"✅ 成功加载文件，共 {len(df)} 行有效数据。")
    except Exception as e:
        st.error("❌ 读取文件失败，请检查是否为正常的 Excel 表格！")
        st.stop()

    # --- 区域卡片 2：设置条件 ---
    with st.container(border=True):
        st.subheader("第二步：设置过滤条件")

        if 'condition_count' not in st.session_state:
            st.session_state.condition_count = 1

        conditions = []

        for i in range(st.session_state.condition_count):
            if i == 0:
                col1, col2, col3 = st.columns([1.5, 1.5, 2])
                logic = "并且 (AND)"
            else:
                col0, col1, col2, col3 = st.columns([1, 1.5, 1.5, 2])
                with col0:
                    logic = st.selectbox("逻辑", ["并且 (AND)", "或者 (OR)"], key=f"logic_{i}",
                                         label_visibility="collapsed")

            with col1:
                field = st.selectbox("字段", options=df.columns, key=f"field_{i}",
                                     label_visibility="collapsed" if i > 0 else "visible")
            with col2:
                operator = st.selectbox("条件", options=["等于", "不等于", "包含", "大于", "小于", "不为空"],
                                        key=f"op_{i}", label_visibility="collapsed" if i > 0 else "visible")
            with col3:
                disabled = (operator == "不为空")
                value = st.text_input("值", key=f"val_{i}", disabled=disabled,
                                      label_visibility="collapsed" if i > 0 else "visible")

            conditions.append({"logic": logic, "field": field, "operator": operator, "value": value})

        if st.button("➕ 继续添加条件"):
            st.session_state.condition_count += 1
            st.rerun()

    # --- 区域卡片 3：附加选项 ---
    with st.expander("⚙️️ 附加统计功能 (选填)"):
        stat_enabled = st.checkbox("开启极简统计")
        if stat_enabled:
            stat_col1, stat_col2 = st.columns(2)
            with stat_col1:
                stat_field = st.selectbox("想统计哪一列？", options=df.columns)
            with stat_col2:
                stat_method = st.selectbox("计算方式", options=["求和", "平均值", "最大值", "最小值", "计数"])

    st.divider()

    # --- 开始处理 ---
    if st.button("🚀 一键提取数据", type="primary", use_container_width=True):
        masks = []
        valid_logics = []

        for cond in conditions:
            f, op, v, l = cond["field"], cond["operator"], cond["value"], cond["logic"]
            if op != "不为空" and not str(v).strip(): continue

            current_mask = pd.Series(False, index=df.index)
            try:
                if op == "等于":
                    current_mask = df[f].astype(str) == str(v)
                elif op == "不等于":
                    current_mask = df[f].astype(str) != str(v)
                elif op == "包含":
                    current_mask = df[f].astype(str).str.contains(str(v), na=False)
                elif op == "不为空":
                    current_mask = df[f].notna()
                elif op in ["大于", "小于"]:
                    temp_num = pd.to_numeric(df[f], errors='coerce')
                    if op == "大于":
                        current_mask = temp_num > float(v)
                    elif op == "小于":
                        current_mask = temp_num < float(v)
                masks.append(current_mask)
                valid_logics.append(l)
            except Exception:
                pass

        if len(masks) == 0:
            filtered_df = df.copy()
        else:
            final_mask = masks[0]
            for idx in range(1, len(masks)):
                if valid_logics[idx] == "并且 (AND)":
                    final_mask = final_mask & masks[idx]
                else:
                    final_mask = final_mask | masks[idx]
            filtered_df = df[final_mask]

        # --- 区域卡片 4：结果交付 ---
        with st.container(border=True):
            st.subheader("📊 提取结果")
            st.success(f"处理完毕！从原表 {len(df)} 行中，为您提取出 {len(filtered_df)} 行符合要求的数据。")

            if stat_enabled and not filtered_df.empty:
                try:
                    temp_series = pd.to_numeric(filtered_df[stat_field], errors='coerce').dropna()
                    res = None
                    if stat_method == "求和":
                        res = temp_series.sum()
                    elif stat_method == "平均值":
                        res = round(temp_series.mean(), 2)
                    elif stat_method == "最大值":
                        res = temp_series.max()
                    elif stat_method == "最小值":
                        res = temp_series.min()
                    elif stat_method == "计数":
                        res = filtered_df[stat_field].count()
                    st.info(f"💡 **快捷统计**：提取的数据中，【{stat_field}】的总【{stat_method}】为：**{res}**")
                except Exception:
                    st.warning("⚠️ 所选列非纯数字，无法进行计算。")

            st.dataframe(filtered_df.head(100))

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                filtered_df.to_excel(writer, index=False, sheet_name='筛选结果')

            # 使用大按钮铺满屏幕
            st.download_button(
                label="📥 立即下载提取后的 Excel",
                data=output.getvalue(),
                file_name="目标数据提取.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )