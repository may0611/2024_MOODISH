import numpy as np
import pandas as pd

file_path = 'data.csv'
df = pd.read_csv(file_path)
print(df)
df = df.dropna()
df = df_filtered = df[df.iloc[:, 2] >= 10000]
df = df.drop_duplicates(subset=df.columns[1], keep='first')


new_column_names = ['id', 'name', 'view', 'reccomend','method', 'type', 'type2','type3','ingredient','inbun','difficult','time']

df.columns = new_column_names

df['happy'] = 0
df['board'] = 0
df['tired'] = 0
df['stress'] = 0
df['sad'] = 0

print(df)

output_csv_path = 'recipe_data.csv'
df.to_csv(output_csv_path, index=False)
