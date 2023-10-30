import pandas as pd
import sys
import gzip
import statistics as stat


"""
AGE00147708\|UZM00038618\|UZM00038457\|USW00094967\|USW00094728
standard out will look like: AGE00147719,180

Powershell equiv:
gc log.txt | select -first 10 # head
gc -TotalCount 10 log.txt     # also head
gc log.txt | select -last 10  # tail
gc -Tail 10 log.txt           # also tail (since PSv3), also much faster than above option
gc log.txt | more             # or less if you have it installed
gc log.txt | %{ $_ -replace '\d+', '($0)' }         # sed
"""
#df = pd.DataFrame(columns=['station','tmax'])
#data=pd.read_csv(sys.stdin)

# I want to take in the stndr out into a dataframe- input is from a file from a particular year
# then find the mean of each station and the mean
# df = pd.read_csv(sys.stdin,names=['station','tmax'], header=None)
# print(df)
wthrData={}

for line in sys.stdin:
    # Strip trailing newline character and split the line into station ID and data
    station, date, data = line.strip().split(',')
    # Extract the first 3 characters from the station ID as a key for the weather station
    # If the key already exists in the dictionary, append the data to its corresponding list
    dateYr = date[0:4]
    if station in wthrData:
        wthrData[station].append(float(data))
    # Otherwise, create a new list for the key and append the data to it
    else:
        wthrData[station] = [float(data)]

#print(wthrData)

# Convert the dictionary to a pandas DataFrame
df = pd.DataFrame.from_dict(wthrData, orient='index')

df= pd.DataFrame.transpose(df)

dfmed = df.median()

for i, r in dfmed.items():
    print(dateYr+","+f"{i},{r}")

#dfmed = dfmed.to_string()

#dfmed.to_csv('testOut.csv', index=False)

#pass year
#pass station medians
