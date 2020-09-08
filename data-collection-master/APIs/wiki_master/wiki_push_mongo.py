import pymongo
import pandas as pd
from tqdm import tqdm
import random
import math

client_sc = pymongo.MongoClient('mongodb+srv://SingleCity:ZflztzKGSP3Nq2qX@singlecity-iw1ea.mongodb.net/test?retryWrites=true&w=majority')
db_sc = client_sc.SingleCity
table_sc = db_sc.table_sc


with open('data/city_ids.json', 'r') as f:
    jcity = json.load(f, parse_float = decimal.Decimal)
    for city in jcity:
        city_list = list(jcity.keys())

def city2page(name):
    path = f'data/pages/{name}'
    with open(path, 'rb') as fp:
        return pickle.load(fp)

unknown = []
def amend_city(id):
    q = { '_id':id }
    old_rec = tbl.find_one(q)
    if old_rec is not None:
        city_name = old_rec['name_with_com']
        row = df[df['City'] == city_name]
        if row.shape[0] == 0:
            unknown.append(city_name)
        else:
            tbl.update_one(q, {'$set':pretty_data(row.iloc[0])})


for id in tqdm(range(29000)):
    amend_city(id)

with open('unknowns.txt', 'w') as fp:
    fp.write('\n'.join(unknown))