import pandas
from pandas.io import sql
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

pandas.set_option('max_columns', 50)

# d = {'Chicago': 1000, 'New York': 1300, 'Portland': 900, 'San Francisco': 1100,
#      'Austin': 450, 'Boston': None}
#
# cities = pandas.Series(d)
#
# print(cities)
#
# print("\n")
#
# print(cities['Chicago'])
#
# print("\n")
#
# print(cities[['Chicago', 'Portland', 'San Francisco']])
#
# print("\n")
#
# print(cities[cities < 1000])
#
# print("\n")
#
# print('Seattle' in cities)
# print('San Francisco' in cities)


data = {'year': [2010, 2011, 2012, 2011, 2012, 2010, 2011, 2012],
        'team': ['Bears', 'Bears', 'Bears', 'Packers', 'Packers', 'Lions', 'Lions', 'Lions'],
        'wins': [11, 8, 10, 15, 11, 6, 10, 4],
        'losses': [5, 8, 6, 1, 5, 10, 6, 12]}

football = pandas.DataFrame(data, columns=['year', 'team', 'wins', 'losses'])

#print(football)

#print("\n")

df = pandas.read_csv("/Users/admin/Documents/Work/AAIHC/AAIHC-Python/Scratchwork/Countries.csv", sep=",")

print(df.columns.values)

print(df[df['Name'] == "United States"]) # Returns series of true/false values

df.plot()


#print(df[(df >= 2).any(axis=1)])






