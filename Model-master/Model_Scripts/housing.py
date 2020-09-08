import pandas as pd
import joblib
import numpy as np
import requests
from sklearn.neighbors import KDTree
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('data/models/housingmodeldata.csv')

def get_housing(id):
    get = requests.get(f'https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{id}').json()
    population = get['Total Population']
    msmoc = get['Median Selected Monthly Owner Costs with Mortgage']
    rent = get['Median Rent']
    room1 = get['Occupants per room']['1 or less']
    room2 = get['Occupants per room']['1 to one and a half ']
    room3 = get['Occupants per room']['one and a half or more']
    beds1 = get['Housing by bedrooms']['No bedrooms']
    beds2 = get['Housing by bedrooms']['1 bedroom']
    beds3 = get['Housing by bedrooms']['2 bedrooms']
    beds4 = get['Housing by bedrooms']['3 bedrooms']
    beds5 = get['Housing by bedrooms']['4 bedrooms']
    beds6 = get['Housing by bedrooms']['5 bedrooms or more']
    homevacancy = get['Vacancy Rate']['Homeowner vacancy rate']
    rentvacancy = get['Vacancy Rate']['Rental vacancy rate']
    rent1 = get['Rent']['Less than USD 500']
    rent2 = get['Rent']['USD 500 - USD 999']
    rent3 = get['Rent']['USD 1,000 - USD 1,499']
    rent4 = get['Rent']['USD 1,500 - USD 1,999']
    rent5 = get['Rent']['USD 2,000 - USD 2,499']
    rent6 = get['Rent']['USD 2,500 - USD 2,999']
    rent7 = get['Rent']['USD 3,000 or more']
    avg = get['Historical Property Value Data']['Average Home Value']['2019-11']
    
    res = [population, msmoc, rent, room1, room2, room3, beds1, beds2, beds3, beds4, beds5,beds6, homevacancy, rentvacancy, rent1,rent2,rent3,rent4,rent5,rent6,rent7, avg]
    return(res)

scaler = StandardScaler()
scaler.fit(df.values)
data = scaler.transform(df.values)


tree = KDTree(data, leaf_size=10)
tes = np.array([9.71100000e+03, 8.78000000e+02, 6.01000000e+02, 9.22000000e+01,
       6.00000000e+00, 1.90000000e+00, 1.40000000e+00, 1.08000000e+01,
       2.60000000e+01, 5.00000000e+01, 1.05000000e+01, 1.30000000e+00,
       3.00000000e+00, 1.29000000e+01, 3.07000000e+01, 6.93000000e+01,
       0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
       0.00000000e+00, 1.30024889e+05]).reshape(1,-1)

test = scaler.transform(tes)

tree.query(test, k=6)[1][0]
for i in tree.query(test, k=6)[1][0]:
    print(requests.get(f'https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{i}').json()['name_with_com'], i)

joblib.dump(tree, 'housing_model.joblib')
joblib.dump(scaler, 'housing_scaler.joblib')
nn = joblib.load('housing_model.joblib')
lscale = joblib.load('housing_scaler.joblib')
tt = lscale.transform(tes)
for i in nn.query(tt, k=6)[1][0]:
    print(requests.get(f'https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{i}').json()['name_with_com'], i)

print(nn.query(tt, k=6)[1][0].tolist())