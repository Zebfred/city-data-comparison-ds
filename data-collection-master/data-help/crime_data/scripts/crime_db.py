import pandas as pd
import numpy as np
import json
from pymongo import MongoClient
from decouple import config
MONGO_URI = config('MONGO_URI')

# import the state and national crime data
df = pd.read_csv("http://s3-us-gov-west-1.amazonaws.com/cg-d4b776d0-d898-4153-90c8-8336f86bdfec/estimated_crimes_1979_2018.csv")

# in the csv, non labelled states are national averages
df['state_abbr'] = df['state_abbr'].replace(np.nan,'US')

#get a list of states from the df
states = df.state_abbr.unique()

# Mississippi has only 24 years of data available, I took it out manually and
# added it to the DB separately
#states = ['MS']
#print(states, '\nlength:',len(states))

client = MongoClient(MONGO_URI)

# iterate through list of states
for s in states:
    to_add = {}
    # iterate through list of years, change manually for Mississippi
    for y in range(1995, 2019):
        vcr = float(df[(df['state_abbr'] == s) & (df['year'] == y)]['violent_crime'].values / df[(df['state_abbr'] == s) & (df['year'] == y)]['population'].values)
        pcr = float(df[(df['state_abbr'] == s) & (df['year'] == y)]['property_crime'].values / df[(df['state_abbr'] == s) & (df['year'] == y)]['population'].values)
        to_add[str(y)] = {'vcr':vcr,
                     'pcr':pcr}
    #insert into database
    to_ins = client.SingleCity.statecrime.insert_one({'_id':s,
                                                     'crime': to_add})
