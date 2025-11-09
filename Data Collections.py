import pandas as pd
import random
import datetime

categories = ['Food', 'Rent', 'Shopping', 'Utilities', 'Transport', 'Entertainment', 'Others']
data = []

for i in range(100):
    date = datetime.date(2025, random.randint(1,10), random.randint(1,28))
    category = random.choice(categories)
    amount = random.randint(100, 5000)
    data.append([date, category, amount])

df = pd.DataFrame(data, columns = ['Date', 'Category', 'Amount'])
df.to_csv('mock_bank_statement.csv', index = False)