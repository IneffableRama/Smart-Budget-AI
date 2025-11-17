import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
file_path = r"C:\Users\Shivam Majhi\Downloads\expense_data_1.csv"
df = pd.read_csv(file_path)

# Basic preprocessing
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df = df[df['Income/Expense'].str.lower() == 'expense']
df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
df = df.dropna(subset=['Date', 'Category', 'Amount'])

# Create Month column
df['Month'] = df['Date'].dt.to_period('M')

# Aggregate monthly expenses by Category
monthly_expense = df.groupby(['Month', 'Category'])['Amount'].sum().reset_index()
monthly_expense['MonthNum'] = monthly_expense['Month'].astype(str).str.replace('-', '').astype(int)

# Set plot style
sns.set_style('darkgrid')

# Plot 1: Monthly expense trend by category
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_expense, x='MonthNum', y='Amount', hue='Category')
plt.title('Monthly Expense Trend by Category')
plt.xlabel('Month Number (YYYY MM)')
plt.ylabel('Amount (INR)')
plt.xticks(rotation=45)
plt.show()

# Plot 2: Expense distribution by category (boxplot)
plt.figure(figsize=(10, 6))
sns.boxplot(data=monthly_expense, x='Category', y='Amount')
plt.title('Expense Distribution by Category')
plt.xticks(rotation=45)
plt.show()

# Plot 3: Pie chart of expense proportions for latest month
latest_month = monthly_expense['MonthNum'].max()
latest_expense = monthly_expense[monthly_expense['MonthNum'] == latest_month]
plt.figure(figsize=(8, 8))
plt.pie(latest_expense['Amount'], labels=latest_expense['Category'], autopct='%1.1f%%', startangle=140)
plt.title('Expense Proportions for Latest Month')
plt.show()
