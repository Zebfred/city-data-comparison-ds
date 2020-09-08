import joblib
from sklearn.neighbors import KDTree
import numpy as np


def housing_render(li, nn):
    feats_arry = np.array(li).reshape(1, -1)
    res_arry = nn.query(feats_arry, k=6)[1][0].tolist()
    return(res_arry[1:])


def get_housing(jsn):
    get = jsn
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

def object_format(obj):
    jsn = {}
    for i in obj:
        jsn[i['name_with_com']] = {'id':i['_id'], 'Latitude': i['Latitude'], 'Longitude': i['Longitude'], 'State': i['State']}
    return(jsn)


def get_industry(jsn):
    get = jsn
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
    res = [construction, manu, wholesale, retail, trans, info, finance, science, education, art, other, admin, health, unempl, income] +  salary + [drivea, com2, com3, com4, com5, time]

    return(res)


def get_culture(jsn):
    get = jsn
    age_dist = list(get['Age Distribution'].values())
    p2010 = get['Population Growth']['2010']
    p2018 = get['Population Growth']['2018']
    if p2010 != 0 and p2018 != 0:
        popgrow = round(((p2018 - p2010) / p2010) * 100, 2)
    else:
        popgrow = 0
    diveristy = list(get['Ethnicity'].values())
    education = list(get['Educational Attainment'].values())
    birth = get['Recent Mothers']['Birth Rate']['Avg']

    res = age_dist + [popgrow, p2018] + diveristy + education + [birth]
    return(res)


def model_render(li, scale, nn, num):
    feats_arry = np.array(li).reshape(1, -1)
    feats_arry_scale = scale.transform(feats_arry)
    res_arry = nn.query(feats_arry_scale, k=6)[1][0].tolist()
    if int(num) in res_arry:
        res_arry.remove(int(num))
    else:
        pass
    return(res_arry)


    return(res)
