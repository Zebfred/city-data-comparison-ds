from __future__ import print_function # Python 2/3 compatibility
import pandas as pd
import boto3
import json
import decimal


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('yesss')

with open('city_ids.json', 'r') as f:
    jcity = json.load(f, parse_float = decimal.Decimal)
    for city in jcity:
        city_list = list(jcity.keys())

        #print("adding city:", city)

                #table.put_item(
                 #  Item={
                #       'year': year,
                #       'title': title,
                #       'info': info,
                #    }
                #)
    #    table.put_item(
    #        Item={
    #        'city':city,
            #'ID': ID,
            #'city_ST':city_ST
    #        }
    #    )
    with open('city_ids.json', 'r') as f:
        jdata = json.load(f, parse_float = decimal.Decimal)
    jdf = pd.DataFrame(data = jdata)
    jdf = jdf.T

    with table.batch_writer() as batch:
        for i in range(0, len(jdf.ID)):
            batch.put_item(
                Item={
                    '_id': jdf.ID[i],
                    'city_st': str(jdf.index[i])
                }
            )



with table.batch_writer() as batch:
    for i in range(len(city_list)):
        batch.put_item(
            Item={
                'city': city_list[i],
                '_id': jdf.ID[i]
            }
            )

'''
with table.batch_writer() as batch:
    for i in range(0, len(jcity)):
        batch.put_item(
            Item={
                'city': city}
        )

        def random_city():
            remaining = os.listdir('pages')
            return random.sample(remaining, 1)[0]

            def city2mid(name):
                return citydata[name]['ID']

            def city2page(name):
                path = f'pages/{name}'
                with open(path, 'rb') as fp:
                    return pickle.load(fp)

            def page2dict(mid, city, summ, sect):
                data = dict(
                    id=mid,
                    city=city,
                    text=text
                )
                for s in sect:
                    data[s.title] = s.text
                return data

            def add2dynamo(data):
                tbl.put_item(Item=data)

            def check_off_city(name):
                a = f'pages/{name}'
                b = f'done/{name}'
                os.rename(a, b)

            def single_city():
                name = random_city()
                mid = city2mid(name)
                page = city2page(name)
                obj = page2dict(mid, name, page.summary, page.sections)
                add2dynamo(obj)
                check_off_city(name)

            single_city()
'''

        #{"Russellville, AL": {"ID": 0, "st": "AL", "state": "Alabama", "lat": 34.5056, "lng": -87.7282, "population": 9711}
