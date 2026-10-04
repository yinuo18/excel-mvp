import pandas as pd
import numpy as np

# 1月数据：比较标准的老实人填法
df_jan = pd.DataFrame({
    "订单号": ["J001", "J002", "J003"],
    "销售员": ["张三", "李四", "王五"],
    "地区": ["华南", "华北", "华东"],
    "销售额": [5000, 8000, 3000]
})

# 2月数据：放飞自我的填法（表头全改了，中间还夹着完全空白的行，甚至多出一列）
df_feb = pd.DataFrame({
    "订单编号": ["F001", np.nan, "F002"],
    "业务员": ["赵六", np.nan, "张三"],
    "区域": ["西南", np.nan, "华南"],
    "销售金额": [6000, np.nan, 4500],
    "备注": ["大客户", np.nan, ""]
})

# 3月数据：不仅表头不一样，数字列里还混进了文字
df_mar = pd.DataFrame({
    "单号": ["M001", "M002"],
    "姓名": ["李四", "测试员"],
    "地区": ["华北", "未知"],
    "销售额": [7200, "暂无数据"]
})

# 批量导出为3个独立的Excel
df_jan.to_excel("1月销售表(标准).xlsx", index=False)
df_feb.to_excel("2月销售表(表头大乱).xlsx", index=False)
df_mar.to_excel("3月销售表(含文字脏数据).xlsx", index=False)

print("✅ 成功生成 3 个用于合并测试的脏Excel，快去网页里测试吧！")