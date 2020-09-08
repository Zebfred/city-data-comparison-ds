import pandas as pd
from sqlalchemy import create_engine

us = pd.read_csv('geoips.csv')
us = us[us.country_code == 'US']

engine = create_engine('')

us.to_sql('geodata', engine)
