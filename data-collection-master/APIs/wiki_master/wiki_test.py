import decimal
import os, pickle, json, random
import pandas as pd
import pymongo
from pymongo import MongoClient
from decouple import config
import wikipediaapi

MONGO_URI = config('MONGO_URI2')
client = MongoClient(MONGO_URI)

with open('./data/city_ids.json', 'r') as f:
    jdata = json.load(f)
jdf = pd.DataFrame(data = jdata)
jdf = jdf.T
# print(jdf.head())

def city2page(name):
    path = f'data/pages/{name}'
    with open(path, 'rb') as fp:
        return pickle.load(fp)

for i in range(0, len(jdf.ID)):
    try:
        ws = city2page(jdf.index[i]).summary
        client.SingleCity.wikidata.insert_one({"_id":jdf.ID[i],
                                                "city_st":jdf.index[i],
                                                "wiki_sum":ws
                                               })
        print(i + 1, jdf.index[i],'inserted')
    except:
        print(jdf.index[i], 'Not found/working...')
#print(city_list)
#print(city_list[0])
# print(city2page(city_list[0]).summary)
#print(city2page('Abbott, TX').summary)
