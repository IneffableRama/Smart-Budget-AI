import pandas as pd
from prophet import Prophet
import plotly.express as px
import streamlit as st
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

# =============================
# STREAMLIT DASHBOARD
# =============================
st.title("Smart Budget AI Dashboard")

# Load data
file_name = "cleaned_transactions_in_inr.xlsx"
df = pd.read_excel(file_name, engine='openpyxl')

# Separate debit (expenses) and credit (income)
df_expenses = df[df['transaction_type'].str.lower() == 'debit']
df_income = df[df['transaction_type'].str.lower() == 'credit']

# =============================
# Overall Expense Forecast
# =============================
st.header("Overall Monthly Expense Forecast")

# Aggregate monthly expenses
monthly_expenses = df_expenses.groupby('month')['amount'].sum().reset_index()
monthly_expenses.rename(columns={'month': 'ds', 'amount': 'y'}, inplace=True)
monthly_expenses['ds'] = pd.to_datetime(monthly_expenses['ds'], format='%Y-%m')

# Train-Test Split for Accuracy
train = monthly_expenses.iloc[:-3]
test = monthly_expenses.iloc[-3:]

# Train Prophet
model_overall = Prophet()
model_overall.fit(train)

# Forecast next 6 months
future_overall = model_overall.make_future_dataframe(periods=6, freq='M')
forecast_overall = model_overall.predict(future_overall)

# Accuracy Metrics
pred_test = forecast_overall.tail(3)['yhat'].values
actual_test = test['y'].values
mae = mean_absolute_error(actual_test, pred_test)
rmse = np.sqrt(mean_squared_error(actual_test, pred_test))
mape = np.mean(np.abs((actual_test - pred_test) / actual_test)) * 100

# Display Accuracy
st.subheader("Model Accuracy")
st.write("**MAE:** INR {:.2f}".format(mae))
st.write("**RMSE:** INR {:.2f}".format(rmse))
st.write("**MAPE:** {:.2f}%".format(mape))

# Show Actual vs Predicted Table
accuracy_df = pd.DataFrame({
    'Month': test['ds'].dt.strftime('%Y-%m'),
    'Actual': actual_test,
    'Predicted': pred_test
})
st.table(accuracy_df)

# Plot overall forecast
fig_overall = px.line(forecast_overall, x='ds', y='yhat', title='Overall Monthly Expense Forecast')
fig_overall.add_scatter(x=monthly_expenses['ds'], y=monthly_expenses['y'], mode='markers', name='Actual')
st.plotly_chart(fig_overall)

# Download forecast
csv_overall = forecast_overall[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(index=False)
st.download_button("Download Overall Forecast CSV", csv_overall, "overall_forecast.csv", "text/csv")

# =============================
# Category-wise Forecast
# =============================
st.header("Category-wise Expense Forecast")
selected_category = st.selectbox("Select a Category", df_expenses['category'].unique())

cat_group = df_expenses[df_expenses['category'] == selected_category]
cat_monthly = cat_group.groupby('month')['amount'].sum().reset_index()

if len(cat_monthly) >= 2:
    cat_monthly.rename(columns={'month': 'ds', 'amount': 'y'}, inplace=True)
    cat_monthly['ds'] = pd.to_datetime(cat_monthly['ds'], format='%Y-%m')

    model_cat = Prophet()
    model_cat.fit(cat_monthly)

    future_cat = model_cat.make_future_dataframe(periods=6, freq='M')
    forecast_cat = model_cat.predict(future_cat)

    fig_cat = px.line(forecast_cat, x='ds', y='yhat', title=f'Forecast for {selected_category}')
    fig_cat.add_scatter(x=cat_monthly['ds'], y=cat_monthly['y'], mode='markers', name='Actual')
    st.plotly_chart(fig_cat)

    # Download category forecast
    csv_cat = forecast_cat[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(index=False)
    st.download_button(f"Download {selected_category} Forecast CSV", csv_cat, f"{selected_category}_forecast.csv", "text/csv")
else:
    st.warning("Not enough data for this category to forecast.")

# =============================
# Income vs Expense Analysis
# =============================
st.header("Income vs Expense Analysis")
monthly_income = df_income.groupby('month')['amount'].sum().reset_index()
monthly_income.rename(columns={'month': 'ds', 'amount': 'income'}, inplace=True)
monthly_income['ds'] = pd.to_datetime(monthly_income['ds'], format='%Y-%m')

combined = pd.merge(monthly_expenses, monthly_income, on='ds', how='outer').fillna(0)
combined['balance'] = combined['income'] - combined['y']

fig_balance = px.bar(combined, x='ds', y=['income', 'y'], barmode='group', title='Income vs Expense')
st.plotly_chart(fig_balance)

# Budget Alert
latest_balance = combined['balance'].iloc[-1]
if latest_balance < 0:
    st.error(f"Alert: Your expenses exceeded income by INR {abs(latest_balance):.2f} last month!")
else:
    st.success(f"Good job! You saved INR {latest_balance:.2f} last month.")
