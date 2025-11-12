import streamlit as st
import pandas as pd

st.title("2024 健保申報藥品數量查詢介面（測試 B 版）")

# 檔案上傳
uploaded_file = st.file_uploader("請上傳藥品資料 CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, encoding="utf-8")

    # 使用者輸入主成分
    keyword = st.text_input("請輸入主成分")

    if keyword:
        # 篩選藥品名稱中包含主成分的項目
        result = df[df["藥品名稱"].str.contains(keyword, case=False, na=False)]

        # 將同藥品名稱的數量加總
        summary = result.groupby(["藥品代碼", "藥品名稱"], as_index=False)["數量"].sum()
        summary.rename(columns={"數量": "總量"}, inplace=True)

        st.write("查詢結果：")
        st.dataframe(summary)

        # 提供下載功能
        csv = summary.to_csv(index=False, encoding="utf-8-sig")
        st.download_button(
            label="下載查詢結果 CSV",
            data=csv,
            file_name="查詢結果.csv",
            mime="text/csv",
        )

