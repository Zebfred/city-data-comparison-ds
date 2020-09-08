import numpy as np
import pandas as pd

# Crime data is collected into two separate csv files. The first contains
# 40 years of data by state, and 10 years (in 10 xls files) by city

# data in this csv contains estimates in instances of no reporting
df = pd.read_csv(
    "http://s3-us-gov-west-1.amazonaws.com/cg-d4b776d0-d898-4153-90c8-8336f86bdfec/estimated_crimes_1979_2018.csv")

# replace null values with 'US'
df['state_abbr'] = df['state_abbr'].replace(np.nan, 'US')

# add violent crime rate (vcr) and property crime rate (pcr) to dataframe
df['vcr'] = df['violent_crime'] / df['population']
df['pcr'] = df['property_crime'] / df['population']

# initialize a new dataframe for exporting

sand = pd.DataFrame(index=None)
sand['state'] = df['state_abbr']
sand['year'] = df['year']
sand['vcr'] = df['vcr']
sand['pcr'] = df['pcr']

# export to csv
sand.to_csv('./crime_data/state_crime.csv', index=False)

# read in xls files, skipping the headers and footers
xl2018 = pd.read_excel(
    './crime_data/Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2018.xls',
    skiprows=3,
    skipfooter=10)
xl2017 = pd.read_excel(
    './crime_data/Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2017.xls',
    skiprows=3,
    skipfooter=10)
xl2016 = pd.read_excel(
    './crime_data/Table_6_Offenses_Known_to_Law_Enforcement_by_State_by_City_2016.xls',
    skiprows=3,
    skipfooter=11)
xl2015 = pd.read_excel(
    './crime_data/Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2015.xls',
    skiprows=3,
    skipfooter=10)
xl2014 = pd.read_excel('./crime_data/table-8.xls', skiprows=3, skipfooter=17)
xl2013 = pd.read_excel(
    './crime_data/Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2013.xls',
    skiprows=3,
    skipfooter=10)
xl2012 = pd.read_excel(
    './crime_data/Table_8_Offenses_Known_to_Law_Enforcement_by_State_by_City_2012.xls',
    skiprows=3,
    skipfooter=7)
xl2011 = pd.read_excel(
    './crime_data/table_8_offenses_known_to_law_enforcement_by_state_by_city_2011.xls',
    skiprows=3,
    skipfooter=7)
xl2010 = pd.read_excel('./crime_data/10tbl08.xls', skiprows=3, skipfooter=7)
xl2009 = pd.read_excel('./crime_data/09tbl08.xls', skiprows=3, skipfooter=7)

# build a function to automatically clean the results and add to a new DF for
# import to database


def cleaner(x, year):
    """
    Takes a dataframe, changes state abbreviations, changes state NaNs,
    calculates violent crime and property crime rate and returns it as
    a new DataFrame (city_st, vcr, pcr) for the year passed in
     """
    # create new dataframe
    df = pd.DataFrame(columns=['city', 'vcr_' + year, 'pcr_' + year])

    # clean numbers from state column and put into new df
    df['city'] = x['State'].str.replace(r'\d+', '')
    # clean numbers from city column
    x['City'] = x['City'].str.replace(r'\d+', '')
    # clean column names
    if 'Violent\ncrime' in x.columns:
        x = x.rename(columns={'Violent\ncrime': 'Violent crime',
                              'Property\ncrime': 'Property crime'})

    # remove null values from column
    if x['City'].isnull().sum() >= 1:
        x['City'] = x['City'].replace(np.nan, 'None')

    # replace states with abbreviations
    df['city'] = df['city'].replace({"ALABAMA": "AL", "ALASKA": "AK", "ARIZONA": "AZ",
                                     "ARKANSAS": "AK", "CALIFORNIA": "CA",
                                     "COLORADO": "CO", "CONNECTICUT": "CT",
                                     "DELAWARE": "DE", "DISTRICT OF COLUMBIA": "DC",
                                     "FLORIDA": "FL", "GEORGIA": "GA", "HAWAII": "HI",
                                     "IDAHO": "ID", "ILLINOIS": "IL", "INDIANA": "IN",
                                     "IOWA": "IA", "KANSAS": "KS", "KENTUCKY": "KY",
                                     "LOUISIANA": "LA", "MAINE": "ME", "MARYLAND": "MD",
                                     "MASSACHUSETTS": "MA", "MICHIGAN": "MI",
                                     "MINNESOTA": "MN", "MISSISSIPPI": "MS",
                                     "MISSOURI": "MI", "MONTANA": "MT", "NEBRASKA": "NE",
                                     "NEVADA": "NV", "NEW HAMPSHIRE": "NH",
                                     "NEW JERSEY": "NJ", "NEW MEXICO": "NM",
                                     "NEW YORK": "NY", "NORTH CAROLINA": "NC",
                                     "NORTH DAKOTA": "ND", "OHIO": "OH",
                                     "OKLAHOMA": "OK", "OREGON": "OR",
                                     "PENNSYLVANIA": "PA", "RHODE ISLAND": "RI",
                                     "SOUTH CAROLINA": "SC", "SOUTH DAKOTA": "SD",
                                     "TENNESSEE": "TN", "TEXAS": "TX", "UTAH": "UT",
                                     "VERMONT": "VT", "VIRGINIA": "VA",
                                     "WASHINGTON": "WA", "WEST VIRGINIA": "WV",
                                     "WISCONSIN": "WI", "WYOMING": "WY"})
    # iterate through dataframe, replacing nan values with proper state abbr.
    state = ""
    for i in range(len(df)):
        if pd.notnull(df.at[i, 'city']):
            if df.at[i, 'city'] != state:
                state = df.at[i, 'city']
        elif pd.isnull(df.at[i, 'city']):
            df.at[i, 'city'] = state

    # populate city column 'city, ST'
    for i in range(len(df['city'])):
        df['city'][i] = x['City'][i] + ", " + df['city'][i]

        # populate violent crime rate column
        df['vcr_' + year][i] = x['Violent crime'][i] / x['Population'][i]

        # populate property crime rate column
        df['pcr_' + year][i] = x['Property crime'][i] / x['Population'][i]

    # set the index for later concatenation
    df.set_index('city')
    return df


cl18 = cleaner(xl2018, '2018')
cl17 = cleaner(xl2017, '2017')
cl16 = cleaner(xl2016, '2016')
cl15 = cleaner(xl2015, '2015')
cl14 = cleaner(xl2014, '2014')
cl13 = cleaner(xl2013, '2013')
cl12 = cleaner(xl2012, '2012')
cl11 = cleaner(xl2011, '2011')
cl10 = cleaner(xl2010, '2010')
cl09 = cleaner(xl2009, '2009')

# merge the dataframes
masta = pd.merge(cl18, cl17, how='outer', on='city')
masta2 = pd.merge(cl16, cl15, how='outer', on='city')
masta3 = pd.merge(cl14, cl13, how='outer', on='city')
masta4 = pd.merge(cl12, cl11, how='outer', on='city')
masta5 = pd.merge(cl10, cl09, how='outer', on='city')
master = pd.merge(masta, masta2, how='outer', on='city')
master = pd.merge(master, masta3, how='outer', on='city')
master = pd.merge(master, masta4, how='outer', on='city')
master = pd.merge(master, masta5, how='outer', on='city')

# export data
master.to_csv('./crime_data/crime.csv', index=False)
