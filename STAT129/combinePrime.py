import pandas as pd
import matplotlib.pyplot as plt
import sys
import gzip as gz
import statistics as stat


# this was the test I did to figure out how to get pandas, jupyter notebook, and matplotlib to work
"""
df = pd.read_csv('C:\\Users\\mikeb\\Documents\\Stat129\\2022tiny.csv')
#print(df)
lines = df.plot.line(x='63', y='20220901')

plt.show
"""

df = pd.read_csv("out327put.csv", header=None) 
df.columns = ["year", "station", "tempInC"]
df["tempInC"] = df["tempInC"] / 10


"""df['temp_change'] = df['tempInC'] - df.groupby('station')['tempInC'].transform('median')
grouped = df.groupby('station')

# Plot the temperature for each station
for name, group in df:
    plt.plot(group['year'], group['temp_change'], label=name)
"""

station_median = df.groupby("station")["tempInC"].median()

# Subtract the median temperature from the temperature values for each station and year
df["temp_change"] = df.apply(lambda x: x["tempInC"] - station_median[x["station"]], axis=1)

grouped = df.groupby('station')

for name, group in grouped:
    plt.plot(group['year'], group['temp_change'], label=name)

"""
plt.xlabel('Year')
plt.ylabel('Temperature (C)')
plt.legend(title="Stations")
plt.show()
"""