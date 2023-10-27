import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('2022tiny.csv')
#print(df)
lines = df.plot.line(x='20220901', y='63')

plt.show