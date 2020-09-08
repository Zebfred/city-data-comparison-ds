import pymongo
import pandas as pd
from tqdm import tqdm
import random
import math

client = pymongo.MongoClient('mongodb+srv://citrus_user:vKzJUUJZg6DXBGvn@cluster0-ak1hs.mongodb.net/test?retryWrites=true&w=majority')
db = client.test
tbl = db.table_name

df = pd.read_csv('data/df_extra_clean.csv', low_memory=False)

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