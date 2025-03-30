import pandas as pd
import plotly.express as px

df1 = pd.read_csv('darkodata.csv')
df2 = pd.read_csv('salarydata.csv')

df1 = df1.merge(df2[['Player', '2024-25']], on='Player', how='left')

df1 = df1.dropna(subset=['2024-25', 'DPM'])
df1['DPM'] = df1['DPM'].astype(float)
df1['2024-25'] = df1['2024-25'].replace('[\$,]', '', regex=True).astype(float)

df1['Value'] = df1['DPM'] / df1['2024-25']

best_value = df1.nlargest(5, 'Value')
worst_value = df1.nsmallest(5, 'Value')

print("Best Value Contracts:")
print(best_value[['Player', '2024-25', 'DPM', 'Value']])

print("\nWorst Value Contracts:")
print(worst_value[['Player', '2024-25', 'DPM', 'Value']])

fig1 = px.scatter(
    df1,
    x='2024-25',
    y='DPM',
    hover_name='Player',
    title='2024-25 Salary vs. DPM with Trend Line',
    labels={'2024-25': '2024-25 Salary ($)', 'DPM': 'DPM'},
    log_x=True,
    template='plotly_dark',
    trendline='ols'
)

best_worst = pd.concat([best_value, worst_value])

fig1.add_trace(px.scatter(
    best_worst,
    x='2024-25',
    y='DPM',
    hover_name='Player',
    color=['Best Value'] * len(best_value) + ['Worst Value'] * len(worst_value),
    size=[5] * len(best_worst),
).data[0])

fig1.show()