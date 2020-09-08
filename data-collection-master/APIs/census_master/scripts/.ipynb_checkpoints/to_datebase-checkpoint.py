import pandas as pd
import os
from math import cos, asin, sqrt
import pymongo
import numpy as np

mongokey = ""
client = pymongo.MongoClient(mongokey)
db = client.citydata
table = db.alldata
print('connected to mongodb')



#load in main census data
df = pd.read_csv('data/census/no_missing_cens.csv', low_memory=False)
print('Cenesus data loaded...')

#load the census reference data
df_ref = pd.read_csv('data/census/complete_min_data.csv')
print('Reference dataset loaded..')


#get the path for the zillow datasets
zillow_path = 'data/housing/zillow_city/'
zillow_files = os.listdir('data/housing/zillow_city/')
zillow_names = [i.split('.csv')[0].split('City_')[1] for i in zillow_files]

#load in the zillow housing by city data sets
for i in zillow_files:
    name = i.split('.csv')[0].split('City_')[1]
    vars()[name] = pd.read_csv(zillow_path + i, encoding = 'latin')
    full_name = [f"{i[0]} {i[1]}" for i in vars()[name][['RegionName', 'State']].values]
    vars()[name]['full_name'] = full_name

print('Zillow datasets loaded...')

#load the zillow zipcode with lon and lat dataset
zillow_zips = pd.read_csv('data/housing/zipcode_reference/zillow_allhomes_zipcodes_loc.csv')
print('Zillow zips loaded...')


housing_dates = pd.read_csv('data/json/housing_dates.csv')
housing_dates = housing_dates['dates'].values.tolist()

print('Housing dates loaded..')


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(a))


for nm in range(len(df)):
    if df_ref['all_housing_present'][nm] == True:
        all_city_present = True
    else:
        all_city_present = False
    if df_ref['all_housing_bedrooms_present'][nm] == True:
        all_city_bedrooms_present = True
    else:
        all_city_bedrooms_present = False


    if df_ref['all_housing_missing'][nm] == True:
        has_onebed = True
        city_data_availible = False
        no_city_data = True
        Zhvi_1bedroom_dict = None
        Zhvi_2bedroom_dict = None
        Zhvi_3bedroom_dict = None
        Zhvi_4bedroom_dict = None
        Zhvi_5Bedroom_dict = None
        st = df_ref['st'][nm]
        zip_state = zillow_zips[zillow_zips['State'] == st]
        clat = zip_state.lat.values
        clng = zip_state.lng.values
        set_lat = df_ref['lat'][nm]
        set_lng =  df_ref['lng'][nm]
        mapper = []
        for loc in range(len(clat)):
            dist_val = distance(set_lat, set_lng, clat[loc], clng[loc])
            mapper.append(dist_val)
        index_min = np.argmin(mapper)
        ref_zip = zip_state.iloc[index_min]['RegionName']
        ref_county = zip_state.iloc[index_min]['CountyName']
        ref_city = zip_state.iloc[index_min]['City']
        note = 'none'
        Zhvi_AllHomes_dict = {}
        note = f"Property value data corresponds with zipcode {ref_zip} in {ref_county}."
        house_prices_val = zillow_zips[zillow_zips.RegionName == ref_zip][housing_dates].values[0]
        for price in range(len(housing_dates)):
            Zhvi_AllHomes_dict[housing_dates[price]] = float(house_prices_val[price])

    else:
        cit = df['full_name'][nm]
        no_city_data = False
        note = f"Property value data for {cit} provided by Zillow."
        for room_name in zillow_names:
            if df_ref[room_name][nm] == True:
                vars()[room_name.split('Zhvi')[1]] = True
                city_full_name = df_ref['full_name'][nm]
                bed_vals = vars()[room_name][vars()[room_name].full_name == city_full_name][housing_dates].values[0]
                bed_vals = [None if str(i) == 'nan' else i for i in bed_vals]
                bedroom_dynamic_value = room_name + '_dict'
                vars()[bedroom_dynamic_value] = {}
                for price in range(len(housing_dates)):
                    vars()[bedroom_dynamic_value][housing_dates[price]] = bed_vals[price]
            else:
                bedroom_dynamic_value = room_name + '_dict'
                vars()[room_name.split('Zhvi')[1]] = False
                vars()[bedroom_dynamic_value]= None
    jsn =   {'_id':nm,
        'name_with_com':df_ref['name_comm'][nm],
        'city_no_st':df_ref['only_city'][nm],
        'census_full_name':df.NAME[nm],
        'City': df.full_name[nm],
        'State': df.state[nm],
        'st': df.st[nm],
        'geo_id':df.GEO_ID[nm],
        'Latitude': float(df.lat[nm]),
        'Longitude': float(df.lng[nm]),
        'Total Population':float(df['pop2018'][nm]),
        'Population Male & Female':{'Male':float(df['DP05_0002PE'][nm]),'Female':float(df['DP05_0003PE'][nm])},
        'Age Distribution':{'Under 5':float(df['DP05_0005PE'][nm]),
            '5 to 9':float(df['DP05_0006PE'][nm]),
            '10 to 14':float(df['DP05_0007PE'][nm]),
            '15 to 19':float(df['DP05_0008PE'][nm]),
            '20 to 24':float(df['DP05_0009PE'][nm]),
            '25 to 34':float(df['DP05_0010PE'][nm]),
            '35 to 44':float(df['DP05_0011PE'][nm]),
            '45 to 54':float(df['DP05_0012PE'][nm]),
            '55 to 59':float(df['DP05_0013PE'][nm]),
            '60 to 64':float(df['DP05_0014PE'][nm]),
            '65 to 74':float(df['DP05_0015PE'][nm]),
            '75 to 84':float(df['DP05_0016PE'][nm]),
            '85 years and over': float(df['DP05_0017PE'][nm])},
        'Median Age': float(df['DP05_0018E'][nm]),
        'Population under 18':float(df['DP05_0019PE'][nm]),
        'Population over 16':float(df['DP05_0020PE'][nm]),
        'Ethnicity':{'White':float(df['DP05_0077PE'][nm]),
            'Hispanic or Latino':float(df['DP05_0071PE'][nm]),
            'African American':float(df['DP05_0078PE'][nm]),
            'American Indian':float(df['DP05_0079PE'][nm]),
            'Asian':float(df['DP05_0080PE'][nm]),
            'Pacific Islander':float(df['DP05_0081PE'][nm]),
            'other race':float(df['DP05_0082PE'][nm]),
            'Two or more races':float(df['DP05_0083PE'][nm])},
        'Marital Status':{'Males':{'Never Married':float(df['DP02_0025PE'][nm]),
                                  'Currently Married':float(df['DP02_0026PE'][nm]),
                                  'Separated':float(df['DP02_0027PE'][nm]),
                                  'Divorced':float(df['DP02_0028PE'][nm])},
                        'Females':{'Never Married':float(df['DP02_0031PE'][nm]),
                                  'Currently Married':float(df['DP02_0032PE'][nm]),
                                  'Separated':float(df['DP02_0033PE'][nm]),
                                  'Divorced':float(df['DP02_0034PE'][nm])}
                        },
        'Recent Mothers':{'Total':float(df['DP02_0036E'][nm]),
                        'Birth Rate':{'Avg':float(df['DP02_0039E'][nm])},
                        'Age Distribution':{'15-19':float(df['DP02_0040E'][nm]),
                                           '20-34':float(df['DP02_0041E'][nm]),
                                           '35-50':float(df['DP02_0042E'][nm])},
                        'National Avg':{'15-19':17.29,
                                           '20-34':103.95,
                                           '35-50':19.82}},
        'School Enrollment':{'Preschool':float(df['DP02_0054PE'][nm]),
                           'Elementary':float(df['DP02_0055PE'][nm]),
                           'High school':float(df['DP02_0056PE'][nm]),
                           'College':float(df['DP02_0057PE'][nm])},
        'Educational Attainment':{'Less than 9th grade':float(df['DP02_0059PE'][nm]),
                           '9th to 12th grade no diploma':float(df['DP02_0060PE'][nm]),
                           'High school':float(df['DP02_0061PE'][nm]),
                           'Some college no degree':float(df['DP02_0062PE'][nm]),
                            "Associate's degree":float(df['DP02_0063PE'][nm]),
                           "Bachelor's degree":float(df['DP02_0064PE'][nm]),
                           'Graduate degree':float(df['DP02_0065PE'][nm])},
        'Language':{'English Only':float(df['DP02_0111PE'][nm]),'Language other than English':float(df['DP02_0112PE'][nm]),'Cannot Speak English':float(df['DP02_0113PE'][nm])},
        'Two or more Languages': float(df['DP02_0112PE'][nm]) - float(df['DP02_0113PE'][nm]),
        'Unemployment Rate': float(df['DP03_0009PE'][nm]),
        'Sex of Labor Force': {'Male': 100 - float(df['DP03_0011PE'][nm]), 'Female':float(df['DP03_0011PE'][nm])},
        'Commuting to Work': {'Drives Alone':float(df['DP03_0019PE'][nm]),
                            'Carpools':float(df['DP03_0020PE'][nm]),
                            'Public Transport':float(df['DP03_0021PE'][nm]),
                            'Walks':float(df['DP03_0022PE'][nm]),
                            'Works at home':float(df['DP03_0024PE'][nm]),
                            "Other transport":float(df['DP03_0023PE'][nm])},
        'Mean Travel Time': float(df['DP03_0025E'][nm]),
        'Occupation':{'Management business science and arts occupations':float(df['DP03_0027PE'][nm]),'Service occupations':float(df['DP03_0028PE'][nm]),'Sales and office occupations':float(df['DP03_0029PE'][nm]),'Natural resources construction and maintenance occupations':float(df['DP03_0030PE'][nm])},
        'Industry':{'Agriculture forestry fishing and hunting and mining':float(df['DP03_0033PE'][nm]),

        'Construction':float(df['DP03_0034PE'][nm]),
        'Manufacturing':float(df['DP03_0035PE'][nm]),
        'Wholesale trade':float(df['DP03_0036PE'][nm]),
        'Retail trade':float(df['DP03_0037PE'][nm]),
        'Transportation and warehousing and utilities':float(df['DP03_0038PE'][nm]),
        'Information':float(df['DP03_0039PE'][nm]),
        'Finance and insurance and real estate and rental and leasing':float(df['DP03_0040PE'][nm]),
        'Professional scientific and management and administrative and waste management services':float(df['DP03_0041PE'][nm]),
        'Educational services and health care and social assistance':float(df['DP03_0042PE'][nm]),
        'Arts entertainment and recreation and accommodation and food services':float(df['DP03_0043PE'][nm]),
        'Other services except public administration':float(df['DP03_0044PE'][nm]),
        'Public administration':float(df['DP03_0045PE'][nm])},


        'Class of Worker':{'Private wage and salary workers':float(df['DP03_0047PE'][nm]),
                          'Government workers':float(df['DP03_0048PE'][nm]),
                          'Self-employed in own not incorporated business workers':float(df['DP03_0049PE'][nm]),
                          'Unpaid family workers':float(df['DP03_0050PE'][nm])},

        'Household Income':{'Less than USD 10,000':float(df['DP03_0052PE'][nm]),

        'USD 10,000 - USD 14,999':float(df['DP03_0053PE'][nm]),
        'USD 15,000 - USD 24,999':float(df['DP03_0054PE'][nm]),
        'USD 25,000 - USD 34,999':float(df['DP03_0055PE'][nm]),
        'USD 35,000 - USD 49,999':float(df['DP03_0056PE'][nm]),
        'USD 50,000 - USD 74,999':float(df['DP03_0057PE'][nm]),
        'USD 75,000 - USD 99,999':float(df['DP03_0058PE'][nm]),
        'USD 100,000 - USD 149,999':float(df['DP03_0059PE'][nm]),
        'USD 150,000 - USD 199,999':float(df['DP03_0060PE'][nm]),
        'USD 200,000 or more':float(df['DP03_0061PE'][nm])},

        'Median Household Income':float(df['DP03_0062E'][nm]),
        'Mean Household Income':float(df['DP03_0063E'][nm]),

        'Retirement Percent':{'With Social Security':float(df['DP03_0066PE'][nm]),
            'With retirement income':float(df['DP03_0068PE'][nm]),
            'With Supplemental Security Income':float(df['DP03_0070PE'][nm])},

        'Retirement Avg':{'Mean Social Security income':float(df['DP03_0067E'][nm]),
                        'Mean retirement income':float(df['DP03_0069E'][nm]),
                        'Mean Supplemental Security Income':float(df['DP03_0071E'][nm])},

        'Public Assistance Percent':{'With cash public assistance income':float(df['DP03_0072PE'][nm]),
                                    'With Food Stamp/SNAP benefits':float(df['DP03_0074PE'][nm])},

        'Median Per Capita Income': float(df['DP03_0092E'][nm]),

        'Per Capita by Gender':{'Female':float(df['DP03_0094E'][nm]), 'Male':float(df['DP03_0093E'][nm])},

        'Health Insurance':float(df['DP03_0096PE'][nm]),
        'Below Poverty Level':float(df['DP03_0119PE'][nm]),
        'Total Housing Units': float(df['DP04_0001E'][nm]),
        'Occupied Housing Units': {'Occupied Housing Units':float(df['DP04_0002PE'][nm]),'Vacant Housing Units':float(df['DP04_0003PE'][nm])},

        'Vacancy Rate':{'Homeowner vacancy rate':float(df['DP04_0004E'][nm]),'Rental vacancy rate':float(df['DP04_0005E'][nm])},

        'Units in Structure': {'1-unit detached':float(df['DP04_0007PE'][nm]),
        '1-unit attached':float(df['DP04_0008PE'][nm]),
        '2 units':float(df['DP04_0009PE'][nm]),
        '3 - 4 units':float(df['DP04_0010PE'][nm]),
        '5 - 9 units':float(df['DP04_0011PE'][nm]),
        '10 - 19 units':float(df['DP04_0012PE'][nm]),
        '20 or more units':float(df['DP04_0013PE'][nm])},

        'Total Housing units':float(df['DP04_0016E'][nm]),
        'Year Built': {'2014 or later':float(df['DP04_0017PE'][nm]),
                     '2010 - 2013':float(df['DP04_0018PE'][nm]),
                     '2000 - 2009':float(df['DP04_0019PE'][nm]),
                     '1990 - 1999':float(df['DP04_0020PE'][nm]),
                     '1980 - 1989':float(df['DP04_0021PE'][nm]),
                     '1970 - 1979':float(df['DP04_0022PE'][nm]),
                     '1960 - 1969':float(df['DP04_0023PE'][nm]),
                     '1950 - 1959':float(df['DP04_0024PE'][nm]),
                     '1940 - 1949':float(df['DP04_0025PE'][nm]),
                     '1939 or earlier':float(df['DP04_0026PE'][nm])},
        'Housing by rooms':{'1 room':float(df['DP04_0028PE'][nm]),
                     '2 rooms':float(df['DP04_0029PE'][nm]),
                     '3 rooms':float(df['DP04_0030PE'][nm]),
                     '4 rooms':float(df['DP04_0031PE'][nm]),
                     '5 rooms':float(df['DP04_0032PE'][nm]),
                     '6 rooms':float(df['DP04_0033PE'][nm]),
                     '7 rooms':float(df['DP04_0034PE'][nm]),
                     '8 rooms':float(df['DP04_0035PE'][nm]),
                     '9 rooms or more':float(df['DP04_0036PE'][nm])},
        'Housing by bedrooms':{'No bedrooms':float(df['DP04_0039PE'][nm]),
                     '1 bedroom':float(df['DP04_0040PE'][nm]),
                     '2 bedrooms':float(df['DP04_0041PE'][nm]),
                     '3 bedrooms':float(df['DP04_0042PE'][nm]),
                     '4 bedrooms':float(df['DP04_0043PE'][nm]),
                     '5 bedrooms or more':float(df['DP04_0044PE'][nm])},
        'Year Moved in':{'2015 or later':float(df['DP04_0051PE'][nm]),
                     '2010 - 2014':float(df['DP04_0052PE'][nm]),
                     '2000 - 2009':float(df['DP04_0053PE'][nm]),
                     '1990 - 1999':float(df['DP04_0054PE'][nm]),
                     '1980 - 1989':float(df['DP04_0055PE'][nm]),
                     '1979 and earlier':float(df['DP04_0056PE'][nm])},
        'Occupants per room':{'1 or less':float(df['DP04_0077PE'][nm]),
                                  '1 to one and a half ':float(df['DP04_0078PE'][nm]),
                                  'one and a half or more':float(df['DP04_0079PE'][nm])},
        'Vehicles Available':{'No vehicles available':float(df['DP04_0058PE'][nm]),
                     '1 vehicle available':float(df['DP04_0059PE'][nm]),
                     '2 vehicles available':float(df['DP04_0060PE'][nm]),
                     '3 or more vehicles available':float(df['DP04_0061PE'][nm])},
        'Selected Monthly Owner Costs with Mortgage':{'Less than USD 500':float(df['DP04_0094PE'][nm]),
                                                    'USD 500 - USD 999':float(df['DP04_0095PE'][nm]),
                                                    'USD 1,000 - USD 1,499':float(df['DP04_0096PE'][nm]),
                                                    'USD 1,500 - USD 1,999':float(df['DP04_0097PE'][nm]),
                                                    'USD 2,000 - USD 2,499':float(df['DP04_0098PE'][nm]),
                                                    'USD 2,500 - USD 2,999':float(df['DP04_0099PE'][nm]),
                                                    'USD 3,000 or more':float(df['DP04_0100PE'][nm])},
        'Median Selected Monthly Owner Costs with Mortgage':float(df['DP04_0101E'][nm]),
        'Selected Monthly Owner Costs without Mortgage':{'Less than USD 250':float(df['DP04_0103PE'][nm]),
                                                    'USD 250 - USD 399':float(df['DP04_0104PE'][nm]),
                                                    'USD 400 - USD 599':float(df['DP04_0105PE'][nm]),
                                                    'USD 600 - USD 799':float(df['DP04_0106PE'][nm]),
                                                    'USD 800 - USD 999':float(df['DP04_0107PE'][nm]),
                                                    'USD 1,000 or more':float(df['DP04_0108PE'][nm])},
        'Median Selected Monthly Owner Costs without Mortgage':float(df['DP04_0109E'][nm]),
        'Rent': {'Less than USD 500':float(df['DP04_0127PE'][nm]),
        'USD 500 - USD 999':float(df['DP04_0128PE'][nm]),
        'USD 1,000 - USD 1,499':float(df['DP04_0129PE'][nm]),
        'USD 1,500 - USD 1,999':float(df['DP04_0130PE'][nm]),
        'USD 2,000 - USD 2,499':float(df['DP04_0131PE'][nm]),
        'USD 2,500 - USD 2,999':float(df['DP04_0132PE'][nm]),
        'USD 3,000 or more':float(df['DP04_0133PE'][nm])},

        'Median Rent':float(df['DP04_0134E'][nm]),
        'Population Growth': {'2010':float(df['pop2010'][nm]),
                             '2011':float(df['pop2011'][nm]),
                             '2012':float(df['pop2012'][nm]),
                             '2013':float(df['pop2013'][nm]),
                             '2014':float(df['pop2014'][nm]),
                             '2015':float(df['pop2015'][nm]),
                             '2016':float(df['pop2016'][nm]),
                             '2017':float(df['pop2017'][nm]),
                             '2018':float(df['pop2018'][nm])},
        'housing_helper': {'note':note,
                           'no_zillow_city_data': no_city_data,
                           'all_city_data_available':all_city_present,
                           'all_bedroom_data_present':all_city_bedrooms_present,
                          'includes_1bed':_1bedroom,
                          'includes_2bed':_2bedroom,
                          'includes_3bed':_3bedroom,
                          'includes_4bed':_4bedroom,
                          'includes_5bed':_5Bedroom,
                          'includes_avgallhomes':_AllHomes},
        'Historical Property Value Data': {'One Bedroom Houses':Zhvi_1bedroom_dict,
                                          'Two Bedroom Houses':Zhvi_2bedroom_dict,
                                          'Three Bedroom Houses':Zhvi_3bedroom_dict,
                                          'Four Bedroom Houses':Zhvi_4bedroom_dict,
                                          'Five Bedroom Houses':Zhvi_5Bedroom_dict,
                                          'Average Home Value':Zhvi_AllHomes_dict}
        }
    table.insert_one(jsn)
