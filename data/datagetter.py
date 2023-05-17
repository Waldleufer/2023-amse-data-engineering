import pandas as pd
from sqlalchemy import create_engine
import datetime

# Step 1: Pull the data

# Source 1
urls_source1 = [
    'https://offenedaten-konstanz.de/sites/default/files/GZ_Grenzverkehr_Jul.%202020-Dez.2021.csv',
    'https://offenedaten-konstanz.de/sites/default/files/TPZ_Grenzverkehr_Juli%202020-M%C3%A4rz%202022.csv',
    'https://offenedaten-konstanz.de/sites/default/files/EmZ_Grenzverkehr_Juli%202020-M%C3%A4rz%202022.csv',
    'https://offenedaten-konstanz.de/sites/default/files/DTV-Grenzverkehr%20KN-Kreuzlingen%202013-2020_0.csv',
]

dfs_source1 = [pd.read_csv(url, sep=",", encoding='ISO-8859-1') for url in urls_source1]

# Source 2
urls_source2 = [
    'https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2020_stuendlich_Wetter.csv',
    'https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2021_stuendlich_Wetter.csv',
]

dfs_source2 = [pd.read_csv(url, sep=",", encoding='ISO-8859-1') for url in urls_source2]

# Step 2: Massage the data

# Convert the 'Datum' and 'Zeit' columns to datetime
for df in dfs_source1:
    if 'Zeit' in df.columns:
        df['Datum'] = pd.to_datetime(df['Datum'] + ' ' + df['Zeit'], format='%d.%m.%Y %H:%M - %H:%M')
    else:
        df['Datum'] = pd.to_datetime(df['Datum'], format='%d. %B %Y')

# Convert the 'Zeit' column to datetime
for df in dfs_source2:
    df['Zeit'] = pd.to_datetime(df['Zeit'])

# Concatenate all dataframes
df_all_source1 = pd.concat(dfs_source1)
df_all_source2 = pd.concat(dfs_source2)

# Step 3: Store the data

# Create SQLite engine
engine = create_engine('sqlite:///preprocessed-data.db')

# Store the data in SQLite
df_all_source1.to_sql('source1_data', engine, if_exists='replace')
df_all_source2.to_sql('source2_data', engine, if_exists='replace')
