import pandas as pd
from sqlalchemy import create_engine
import sqlite3

# Step 1: Pull the data

# Source 1
url_source_TPZ = 'https://offenedaten-konstanz.de/sites/default/files/TPZ_Grenzverkehr_Juli%202020-M%C3%A4rz%202022.csv'
url_source_EmZ = 'https://offenedaten-konstanz.de/sites/default/files/EmZ_Grenzverkehr_Juli%202020-M%C3%A4rz%202022.csv'

df_source_TPZ = pd.read_csv(url_source_TPZ, sep=";", encoding='ISO-8859-1')
df_source_EmZ = pd.read_csv(url_source_EmZ, sep=";", encoding='ISO-8859-1')

# Source 2
# Source 2
urls_source2 = {
    'https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2020_stuendlich_Wetter.csv': ';',
    'https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2021_stuendlich_Wetter.csv': ',',
}

dfs_source2 = [pd.read_csv(url, sep=sep, encoding='ISO-8859-1') for url, sep in urls_source2.items()]

# Step 2: Massage the data

# Split 'Zeit' column into 'Start Time' and 'End Time'
df_source_TPZ[['Start Time', 'End Time']] = df_source_TPZ['Zeit'].str.split(' - ', expand=True)
df_source_EmZ[['Start Time', 'End Time']] = df_source_EmZ['Zeit'].str.split(' - ', expand=True)

# Convert 'Datum' and 'Start Time' to datetime
df_source_TPZ['Start DateTime'] = pd.to_datetime(df_source_TPZ['Datum'] + ' ' + df_source_TPZ['Start Time'], format='%d.%m.%Y %H:%M')
df_source_EmZ['Start DateTime'] = pd.to_datetime(df_source_EmZ['Datum'] + ' ' + df_source_EmZ['Start Time'], format='%d.%m.%Y %H:%M')

# Convert 'Datum' and 'End Time' to datetime
df_source_TPZ['End DateTime'] = pd.to_datetime(df_source_TPZ['Datum'] + ' ' + df_source_TPZ['End Time'], format='%d.%m.%Y %H:%M')
df_source_EmZ['End DateTime'] = pd.to_datetime(df_source_EmZ['Datum'] + ' ' + df_source_EmZ['End Time'], format='%d.%m.%Y %H:%M')


# Convert the 'Zeit' column to datetime
for df in dfs_source2:
    df['Zeit'] = pd.to_datetime(df['Zeit'])

# combine all dataframes from source 2
df_source2_all = pd.concat(dfs_source2)

# Step 3: Store the data

# Create SQLite engine
connectedDB = sqlite3.connect('preprocessed-data.db')
engine = create_engine('sqlite:///preprocessed-data.db')

# Store the data in SQLite
df_source_TPZ.to_sql('TPZ_data', connectedDB, if_exists='replace', index=False)
df_source_EmZ.to_sql('EmZ_data', connectedDB, if_exists='replace', index=False)
df_source2_all.to_sql('source2_data', connectedDB, if_exists='replace', index=False)

connectedDB.close()
