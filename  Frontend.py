pip install streamlit

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("SmartBudgetAI Dashboard")
df = pd.read_csv('mock_bank_statement.csv')
st.dataframe(df)

summary = df.groupby('Category')['Amount'].sum()
st.bar_chart(summary)

streamlit run app.py