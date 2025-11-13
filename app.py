import streamlit as st
import pandas as pd

st.title("2024 健保申報藥品數量查詢介面（正式版）")

uploaded_file = st.file_uploader("請上傳藥品資料 CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="utf-8")

    keyword = st.text_input("請輸入主成分")

    if keyword:
        # 篩選藥品名稱中包含主成分的項目
        result = df[df["藥品名稱"].str.contains(keyword, case=False, na=False)]

        # 依藥品名稱加總（不同代碼合併）
        summary = result.groupby("藥品名稱", as_index=False)["數量"].sum()
        summary.rename(columns={"數量": "累計總量"}, inplace=True)

        # 數字格式化：小數點後一位
        summary["累計總量"] = summary["累計總量"].round(1)

        # 加上序號欄位，從 1 開始
        summary.insert(0, "序號", range(1, len(summary) + 1))

        st.write("查詢結果（累計總量）：")
        st.dataframe(summary)

        # 顯示每種規格的累計總量
        for name, amount in zip(summary["藥品名稱"], summary["累計總量"]):
            st.write(f"💊 `{name}` 的累計總量為：**{amount:,.1f}**")

        # 顯示所有規格合計
        total_amount = summary["累計總量"].sum()
        st.write(f"📊 主成分『{keyword}』的所有規格總使用量為：**{total_amount:,.1f}**")

        # 提供下載功能
        csv = summary.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="下載查詢結果 CSV",
            data=csv,
            file_name="查詢結果.csv",
            mime="text/csv",
        )
