from __future__ import print_function # Python 2/3 compatibility
import pandas as pd
import boto3
import decimal
import os, pickle, json, random
from tqdm import tqdm
import boto3

ddb = boto3.resource('dynamodb', region_name='us-east-2')
table = ddb.Table('yesss')

with open('data/city_ids.json', 'r') as f:
    jcity = json.load(f, parse_float = decimal.Decimal)
    for city in jcity:
        city_list = list(jcity.keys())

def city2page(name):
    path = f'data/pages/{name}'
    with open(path, 'rb') as fp:
        return pickle.load(fp)

with table.batch_writer() as batch:
    for i in range(len(city_list)):
        try:
             batch.put_item(
            Item={
                'city': city_list[i],
                'text': city2page(city_list[i]).text

            }
            )
        except:
            continue
            print("I broke")
