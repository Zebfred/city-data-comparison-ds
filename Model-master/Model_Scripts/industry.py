import pandas as pd
import numpy as np
import requests
import joblib
from sklearn.neighbors import KDTree
from sklearn.preprocessing import StandardScaler


df = pd.read_csv('data/industry.csv')
hib5 = ['DP03_0052PE','DP03_0053PE','DP03_0054PE','DP03_0055PE','DP03_0056PE']
hia5 = ['DP03_0057PE','DP03_0058PE','DP03_0059PE','DP03_0060PE','DP03_0061PE']

def get_industry(id):
    get = requests.get(f"https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{id}").json()
    construction = get['Industry']['Construction']
    manu = get['Industry']['Manufacturing']
    wholesale = get['Industry']['Wholesale trade']
    retail = get['Industry']['Retail trade']
    trans = get['Industry']['Transportation and warehousing and utilities']
    info = get['Industry']['Information']
    finance = get['Industry']['Finance and insurance and real estate and rental and leasing']
    science = get['Industry']['Professional scientific and management and administrative and waste management services']
    education = get['Industry']['Educational services and health care and social assistance']
    art = get['Industry']['Arts entertainment and recreation and accommodation and food services']
    other = get['Industry']['Other services except public administration']
    admin = get['Industry']['Public administration']
    health = get['Health Insurance']
    unempl = get['Unemployment Rate']
    income = get['Median Per Capita Income']
    salary = []
    for i in list(get['Household Income'].keys()):
        salary.append(get['Household Income'][i])
    drivea = get['Commuting to Work']['Drives Alone']
    com2 = get['Commuting to Work']['Carpools']
    com3 = get['Commuting to Work']['Public Transport']
    com4 = get['Commuting to Work']['Walks']
    com5 = get['Commuting to Work']['Works at home']
    time = get['Mean Travel Time']

    list1 = [construction, manu, wholesale, retail, trans, info, finance, science, education, art, other, admin, health, unempl, income]
    res = [construction, manu, wholesale, retail, trans, info, finance, science, education, art, other, admin, health, unempl, income] +  salary + [drivea, com2, com3, com4, com5, time]
    
    return(res)

cols = ['DP03_0034PE',
       'DP03_0035PE',
       'DP03_0036PE',
       'DP03_0037PE',
       'DP03_0038PE',
       'DP03_0039PE',
       'DP03_0040PE',
       'DP03_0041PE',
       'DP03_0042PE',
       'DP03_0043PE',
       'DP03_0044PE',
       'DP03_0045PE',
       'DP03_0096PE', 
       'DP03_0009PE',
        'DP03_0062E'] + hib5 + hia5 + ['DP03_0019PE',
        'DP03_0020PE',
        'DP03_0021PE',
        'DP03_0022PE',
        'DP03_0024PE',
        'DP03_0025E'
       ]

industry = df[cols]
scaler = StandardScaler()
scaler.fit(industry.values)
data = scaler.transform(industry.values)

tree = KDTree(data, leaf_size=10)
test = scaler.transform(np.array(get_industry(17927)).reshape(1,-1))

for i in tree.query(test, k=6)[1][0]:
    print(requests.get(f'https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{i}').json()['name_with_com'], i)
    
joblib.dump(scaler, 'industry_scaler.joblib')
joblib.dump(tree, 'industry_model.joblib')

lscaler = joblib.load('industry_scaler.joblib')
ltree = joblib.load('industry_model.joblib')

test = lscaler.transform(np.array(get_industry(17927)).reshape(1,-1))

for i in ltree.query(test, k=6)[1][0]:
    print(requests.get(f'https://api.citrics.io/jkekal6d6e5si3i2ld66d4dl/citydata/{i}').json()['name_with_com'], i)