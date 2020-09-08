import decimal
import os, pickle, json, random
import pandas as pd
import pymongo




client_2 = pymongo.MongoClient("mongodb+srv://citrus_user:sM9MrUjDKMzbzYVs@cluster0-ak1hs.mongodb.net/test?retryWrites=true&w=majority")
db_2 = client_2.test
table_2 = db_2.table_name

with open('data/city_ids.json', 'r') as f:
    jcity = json.load(f, parse_float = decimal.Decimal)
    for city in jcity:
        city_list = list(jcity.keys())

def city2page(name):
    path = f'data/pages/{name}'
    with open(path, 'rb') as fp:
        return pickle.load(fp)

mylist = []
for i in range(0, len(city_list)):
    try:

        #mylist.append(city2page(city_list[i]).text)
        #for i in range(29000):
        table_sc.update_one({"_id":i}, {'$set' : {'text' : city2page(city_list[i]).text }})
        print("I am working")

    except:
        continue
'''
df =  pd.DataFrame({
                'city': city_list[i],
                'text': mylist[i]
            })

df = pd.to_csv(r'city-data1/itter_7_dyno/wiki_dataframe/wiki_df.csv')


unknown = []
def amend_city(id):
    q = { '_id':id }
    old_rec = tbl.find_one(q)
    if old_rec is not None:
        #city_name = old_rec['name_with_com']
        #row = df[df['_id'] == city_name]
        if row.shape[0] == 0:
            unknown.append(city_name)
        else:
            tbl.update_one(q, {'$set':pretty_data(row.iloc[0])})


for id in tqdm(range(29000)):
    amend_city(id)
'''
with open('mylist.txt', 'w') as fp:
    fp.write('\n'.join(mylist))
