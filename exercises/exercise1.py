import pandas as pd
import ssl
from sqlalchemy import create_engine

# This will ignore SSL certificate verification
ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv'
data = pd.read_csv(url, sep=";")

# Meaningful column names
data = data.rename(columns={
    'column_1': 'ID',
    'column_2': 'Airport_Name',
    'column_3': 'City',
    'column_4': 'Country',
    'column_5': 'IATA',
    'column_6': 'ICAO',
    'column_7': 'Latitude',
    'column_8': 'Longitude',
    'column_9': 'Altitude',
    'column_10': 'Timezone',
    'column_11': 'DST',
    'column_12': 'Tz_database_time_zone',
    'geo_punkt': 'Geo_Point'
})

engine = create_engine('sqlite:///airports.sqlite')
data.to_sql('airports', engine, if_exists='replace', index=False)