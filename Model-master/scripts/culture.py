import pandas as pd
import numpy as np
import requests
import joblib
from sklearn.neighbors import KDTree
from sklearn.preprocessing import StandardScaler

cultdf = pd.read_csv('data/cultdf.csv')




def get_culture(id):
    get = requests.get(f"https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{id}").json()
    age_dist = list(get['Age Distribution'].values())
    p2010 = get['Population Growth']['2010']
    p2018 = get['Population Growth']['2018']
    p2017 = get['Population Growth']['2017']
    p2016 = get['Population Growth']['2016']
    if p2010 != 0 and p2018 != 0:
        popgrow = round(((p2018 - p2010) / p2010) * 100, 2)
    else:
        popgrow = 0
    diveristy = list(get['Ethnicity'].values())
    education = list(get['Educational Attainment'].values())
    birth = get['Recent Mothers']['Birth Rate']['Avg']
    
    
    res = age_dist + [popgrow, p2016, p2017 p2018] + diveristy + education + [birth]
    return(res)
    
    


scaler = StandardScaler()
scaler.fit(cultdf.values)
data = scaler.transform(cultdf.values)

tree = KDTree(data, leaf_size=10)
test = scaler.transform(np.array(get_culture(17927)).reshape(1,-1))

for i in tree.query(test, k=6)[1][0]:
    print(requests.get(f'https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{i}').json()['name_with_com'], i)
    
joblib.dump(scaler, 'culture_scaler.joblib')
joblib.dump(tree, 'culture_model.joblib')

lscaler = joblib.load('culture_scaler.joblib')
ltree = joblib.load('culture_model.joblib')

test = lscaler.transform(np.array(get_culture(17927)).reshape(1,-1))

for i in ltree.query(test, k=6)[1][0]:
    print(requests.get(f'https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{i}').json()['name_with_com'], i)