import json

with open('venues/ids.json', 'r') as fp:
    bycity = json.load(fp)

print(bycity)