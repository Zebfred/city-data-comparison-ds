import os, json
from tqdm import tqdm

rpath = 'cache/results/'
vens = dict()
invalids = dict()
empties = dict()

with open('citynames.json', 'r') as fp:
    cities = json.load(fp)
with open('city_ids.json', 'r') as fp:
    citydata = json.load(fp)

for fn in tqdm(os.listdir(rpath)):
    with open(rpath + fn, 'r') as fp:
        data = fp.read()
    justcity = fn.split('.')[0]
    fullcity = cities[justcity]
    if data == 'invalid city name':
        invalids[fullcity] = citydata[fullcity]
    elif data == '':
        empties[fullcity] = citydata[fullcity]
    else:
        vens[fullcity] = data.split('\n')

with open ('venues/ids.json', 'w') as fp:
    json.dump(vens, fp)
with open('venues/invalid_cities.json', 'w') as fp:
    json.dump(invalids, fp)
with open('venues/empty_cities.json', 'w') as fp:
    json.dump(empties, fp)