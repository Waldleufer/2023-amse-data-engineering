import pandas as pd
import time
import numpy as np
from sqlalchemy import create_engine

# Step 1: Read the CSV File
# The encoding is set to 'iso-8859-1' to preserve German special characters
# Skip the first 6 and last 4 rows since they contain metadata
# Perform exponential back-off if unsucessful for 4 additional times after the initial call failed.
max_retries = 5
for attempt in range(max_retries):
    try:
        df = pd.read_csv('https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv',
                         sep=";", skiprows=6, skipfooter=4, encoding='UTF-8', engine='python',
                         dtype={'Unnamed: 1': str}) # Convert the type of the second column to string
        break
    except Exception as e:
        if attempt < max_retries - 1:  # i.e. not on last attempt
            wait_time = 2 ** attempt  # exponential back-off
            print(f"Attempt {attempt + 1} failed, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            raise Exception(f"Failed to fetch data after {max_retries} attempts. The last exception was: {str(e)}") from None
# Step 2: Data Filtering and Renaming
# Rename columns based on their index

columns = df.columns.tolist()
indices_to_rename = {
    0: 'date',
    1: 'CIN',
    2: 'name',
    12: 'petrol',
    22: 'diesel',
    32: 'gas',
    41: 'electro',
    52: 'hybrid',
    61: 'plugInHybrid',
    68: 'others'
}
for index, new_name in indices_to_rename.items():
    if index < len(columns):
        columns[index] = new_name
df.columns = columns

# Keep only required columns
df = df[['date', 'CIN', 'name', 'petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']]

# Step 3: Assign fitting datatypes:
# Convert 'date' to datetime
df['date'] = pd.to_datetime(df['date'], format='%d.%m.%Y') # assuming the date format is DD.MM.YYYY

# Convert 'CIN' to string
df['CIN'] = df['CIN'].astype(str)

# 'name' is likely already a string, but this will ensure it
df['name'] = df['name'].astype(str)

# Convert the rest to integer
for column in ['petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']:
    df[column] = pd.to_numeric(df[column], errors='coerce')  # convert values to numeric, replace non-numeric values with NaN
    df[column] = df[column].fillna(0).astype(int)  # replace NaNs with 0, then convert to integer


# Step 4: Data Validation
# "-" should be replaced with NaN.
df = df.replace('-', np.nan)

# CINs must be strings with 5 characters
df = df[df['CIN'].apply(lambda x: isinstance(x, str) and len(x) == 5)]

# All other columns should be positive integers > 0
for column in ['petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']:
    df = df[df[column].apply(lambda x: np.isnan(x) or x > 0)]

# Step 5: Write to SQLite Database
engine = create_engine('sqlite:///cars.sqlite')
df.to_sql('cars', engine, if_exists='replace', index=False)
