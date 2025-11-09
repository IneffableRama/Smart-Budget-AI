from sklearn.linear_model import LinearRegression
import numpy as np

# Monthly spending data
monthly_spend = df.groupby(df['Date'].dt.month)['Amount'].sum().reset_index()
X = monthly_spend[['Date']]
y = monthly_spend['Amount']

model = LinearRegression()
model.fit(X, y)

future_month = np.array([[11]])  # Predict for November
pred = model.predict(future_month)

print("Predicted Spending for Next Month: ₹", round(pred[0], 2))