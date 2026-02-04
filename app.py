import streamlit as st
import pandas as pd
import sqlite3

st.title("📦 Amazon Order Analyzer")
st.write("Upload your Amazon Order History Excel file to see your dashboard.")

# 1. File Uploader
uploaded_file = st.file_uploader("Choose your Amazon Excel file", type=['xlsx'])

if uploaded_file:
    # 2. Load the data
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")
    
    # 3. Show basic stats
    total_spent = df['Total'].sum() if 'Total' in df.columns else 0
    st.metric("Total Lifetime Spend", f"${total_spent:,.2f}")

    # 4. Show a chart
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        chart_data = df.groupby(df['Order Date'].dt.year)['Total'].sum()
        st.subheader("Spending by Year")
        st.bar_chart(chart_data)

    # 5. Show the raw data
    st.subheader("Order Details")
    st.dataframe(df)
