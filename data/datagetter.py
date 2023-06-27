import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import numpy as np


def execute_pipeline():
    # Step 1: Pull the data
    df_source_TPZ, df_source_EmZ, df_source_bikes = pull_data()

    # Step 2: Massage the data
    df_source_TPZ, df_source_EmZ, df_source_bikes, merged_df = massage_data(df_source_TPZ, df_source_EmZ, df_source_bikes)

    # Step 3: Store the data
    store_data(df_source_TPZ, df_source_EmZ, df_source_bikes, merged_df)

    print("Pipeline executed sucessfully")
    

def pull_data():
    # Source 1
    url_source_TPZ = 'https://offenedaten-konstanz.de/sites/default/files/TPZ_Grenzverkehr_Juli%202020-M%C3%A4rz%202022.csv'
    url_source_EmZ = 'https://offenedaten-konstanz.de/sites/default/files/EmZ_Grenzverkehr_Juli%202020-M%C3%A4rz%202022.csv'

    df_source_TPZ = pd.read_csv(url_source_TPZ, sep=";", encoding='ISO-8859-1')
    df_source_EmZ = pd.read_csv(url_source_EmZ, sep=";", encoding='ISO-8859-1')

    # Source 2
    urls_source2 = {
        'https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2020_stuendlich_Wetter.csv': ';',
        'https://offenedaten-konstanz.de/sites/default/files/Zaehlstelle_Herose_2021_stuendlich_Wetter.csv': ',',
    }

    dfs_source2 = [pd.read_csv(url, sep=sep) for url, sep in urls_source2.items()]

    return df_source_TPZ, df_source_EmZ, dfs_source2


def massage_data(df_source_TPZ, df_source_EmZ, dfs_source2):
    # Split 'Zeit' column into 'Start Time' and 'End Time'
    df_source_TPZ[['Start Time', 'End Time']] = df_source_TPZ['Zeit'].str.split(' - ', expand=True)
    df_source_EmZ[['Start Time', 'End Time']] = df_source_EmZ['Zeit'].str.split(' - ', expand=True)

    # Convert 'Datum' and 'Start Time' to datetime
    df_source_TPZ['Start DateTime'] = pd.to_datetime(df_source_TPZ['Datum'] + ' ' + df_source_TPZ['Start Time'], format='%d.%m.%Y %H:%M')
    df_source_EmZ['Start DateTime'] = pd.to_datetime(df_source_EmZ['Datum'] + ' ' + df_source_EmZ['Start Time'], format='%d.%m.%Y %H:%M')

    def convert_to_datetime(date_str):
        if "-" in date_str:
            return pd.to_datetime(date_str, format='%Y-%m-%d %H:%M:%S')
        else:
            return pd.to_datetime(date_str, format='%d.%m.%Y %H:%M')

    # Convert the 'Zeit' column to datetime
    for df in dfs_source2:
        df['Zeit'] = df['Zeit'].apply(convert_to_datetime)

    # Combine all dataframes from source 2
    df_source_bikes = pd.concat(dfs_source2)

    # Only keep Start DateTime and relevant columns
    df_source_EmZ = df_source_EmZ[['Start DateTime', 'EmZCH', 'EmZD']]
    df_source_TPZ = df_source_TPZ[['Start DateTime', 'TPZCH', 'TPZD']]
    df_source_bikes = df_source_bikes[['Zeit', 'FahrradbrueckeFahrradbruecke', 'Symbol Wetter', 'Temperatur (°C)', 'Regen (mm)']]
    
    # Handle lines with null values
    df_source_EmZ = df_source_EmZ.dropna()
    df_source_TPZ = df_source_TPZ.dropna()
    df_source_bikes = df_source_bikes.dropna(subset=["Zeit"])
    df_source_bikes['FahrradbrueckeFahrradbruecke'] = df_source_bikes['FahrradbrueckeFahrradbruecke'].fillna(0)
    df_source_bikes = remove_faulty_periods(df_source_bikes, ['FahrradbrueckeFahrradbruecke'])

    # Use practical types
    df_source_EmZ['EmZCH'] = df_source_EmZ['EmZCH'].astype(int)
    df_source_EmZ['EmZD'] = df_source_EmZ['EmZD'].astype(int)
    df_source_TPZ['TPZCH'] = df_source_TPZ['TPZCH'].astype(int)
    df_source_TPZ['TPZD'] = df_source_TPZ['TPZD'].astype(int)
    df_source_bikes['FahrradbrueckeFahrradbruecke'] = df_source_bikes['FahrradbrueckeFahrradbruecke'].astype(int)

    # Rename weird column names and Unify names
    df_source_bikes.rename(columns={'FahrradbrueckeFahrradbruecke': 'Fahrradbruecke total', 'Zeit': 'Start DateTime'}, inplace=True)

    # Merge datasets using inner join on 'Start DateTime'
    # The inner join only keeps rows that can be filled with data from all three sources.
    merged_df = df_source_TPZ.merge(df_source_EmZ, on='Start DateTime', how='inner').merge(df_source_bikes, on='Start DateTime', how='inner')

    return df_source_TPZ, df_source_EmZ, df_source_bikes, merged_df


def store_data(df_source_TPZ, df_source_EmZ, df_source_bikes, merged_df):
    # Create SQLite engine
    connectedDB = sqlite3.connect('preprocessed-data.sqlite')

    # Store the data in SQLite
    df_source_TPZ.to_sql('TPZ_data', connectedDB, if_exists='replace', index=False)
    df_source_EmZ.to_sql('EmZ_data', connectedDB, if_exists='replace', index=False)
    df_source_bikes.to_sql('bikes_data', connectedDB, if_exists='replace', index=False)
    merged_df.to_sql('merged_data', connectedDB, if_exists='replace', index=False)

    connectedDB.close()


def remove_faulty_periods(df, bike_column):
    """
    This function removes faulty time periods from the dataframe 'df'
    A time period is faulty if all columns ar nan, or there is a steep drop or there are at least 3 consecutive zeros.
    """

    # Defining the steep drop
    steep_drop_before = ((df[bike_column].diff().abs() > 50) & (df[bike_column] == 0)).any(axis=1)
    steep_drop_after = ((df[bike_column].diff(-1).abs() > 50) & (df[bike_column] == 0)).any(axis=1)

    # Defining the sequences of at least 3 consecutive zeros
    consecutive_zeros = df[bike_column].rolling(window=3).apply(lambda x: np.all(x == 0), raw=True).all(axis=1)

    # row without any date
    all_na = df[bike_column].isna().all(axis=1)

    # Combining the two conditions
    df['faulty'] = steep_drop_before | steep_drop_after | consecutive_zeros | all_na

    # Find the start and end times of the faulty periods
    faulty_periods = df.loc[df['faulty'] != df['faulty'].shift().fillna(False), ['Zeit', 'faulty']]

    # Create dataframes for start and end times separately
    start_times = faulty_periods.loc[faulty_periods['faulty'], 'Zeit']
    end_times = faulty_periods.loc[~faulty_periods['faulty'], 'Zeit']

    # If the last period is faulty and has no end, add the last timestamp of df as its end
    if len(start_times) > len(end_times):
        end_times.loc[len(end_times)] = df['Zeit'].iloc[-1]

    # Print start and end times
    for start, end in zip(start_times, end_times):
        print(f"Faulty period started at {start} and ended at {end}")
        
    # Remove faulty periods
    df = df[~df['faulty']]
    
    # Drop the 'faulty' column as it's not needed anymore
    df = df.drop(columns='faulty')

    return df


if __name__ == '__main__':
    execute_pipeline()
