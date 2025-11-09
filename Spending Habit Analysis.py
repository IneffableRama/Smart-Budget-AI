summary = df.groupby('Category')['Amount'].sum().sort_values(ascending = False)
print(summary)

# Visualization
import matplotlib.pyplot as plt
summary.plot(kind = 'bar')
plt.title('Spending by Category')
plt.show()