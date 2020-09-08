import decimal
import os, pickle, json, random
import pandas as pd

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
        mylist.append(city2page(city_list[i]).text)
        print("I am working")
    except:
        continue    
        
df =  pd.DataFrame({
                'city': city_list[i],
                'text': mylist[i]
            })

df = pd.to_csv(r'city-data1/itter_7_dyno/wiki_dataframe/wiki_df.csv')
