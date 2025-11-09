import pandas as pd

df = pd.read_csv('mock_bank_statement.csv')

# Convert date
df['Date'] = pd.to_datetime(df['Date'])
df['Amount'] = df['Amount'].astype(float)

# Add income/expense column
df['Type'] = df['Amount'].apply(lambda x: 'Expense' if x > 0 else 'Income')

print(df.head())