import os
import ssl
import time
import urllib.request
import zipfile
import pandas as pd
from sqlalchemy import create_engine, BigInteger, Text, Float


def main():
    gtfs_url = 'https://gtfs.rhoenenergie-bus.de/GTFS.zip'
    gtfs_zipfile_name = 'GTFS.zip'
    stops_filename = 'stops.txt'
    stops_columns = ['stop_id', 'stop_name', 'stop_lat', 'stop_lon', 'zone_id']
    zone_id_column = 'zone_id'
    target_zone_id = 2001
    coordinate_columns = ['stop_lat', 'stop_lon']
    sqlite_db_name = 'gtfs.sqlite'
    sqlite_table_name = 'stops'

    download_file_exponential_backoff(gtfs_url, gtfs_zipfile_name)
    extract_file(gtfs_zipfile_name, stops_filename)
    df = load_and_filter_data(stops_filename, stops_columns, zone_id_column, target_zone_id)
    df = validate_data(df, coordinate_columns)
    write_to_sqlite(df, sqlite_db_name, sqlite_table_name)

    # Cleanup: Remove downloaded zip file and extracted text file
    if os.path.exists(gtfs_zipfile_name):
        os.remove(gtfs_zipfile_name)
    if os.path.exists(stops_filename):
        os.remove(stops_filename)


def download_file_exponential_backoff(url, filename, max_retries=5):
    delay = 1  # initial delay is 1 second
    for attempt in range(max_retries):
        try:
            ssl._create_default_https_context = ssl._create_unverified_context
            urllib.request.urlretrieve(url, filename)
            break
        except Exception as e:
            if attempt < max_retries - 1:  # not the last attempt
                time.sleep(delay)
                delay *= 2  # double the delay for next attempt
            else:
                raise e  # re-raise the last exception if all attempts failed


def extract_file(zipfile_name, file_to_extract):
    with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
        zip_ref.extract(file_to_extract)


def load_and_filter_data(filename, columns, filter_column, filter_value):
    df = pd.read_csv(filename, sep=',', usecols=columns)
    df = df[df[filter_column] == filter_value]
    return df


def validate_data(df, lat_lon_columns):
    df = df.dropna()
    for col in lat_lon_columns:
        df = df[df[col].between(-90, 90, inclusive='both')]
    return df


def write_to_sqlite(df, db_name, table_name):
    engine = create_engine(f'sqlite:///{db_name}', echo=True)
    df.to_sql(table_name, con=engine, if_exists='replace', index=False, dtype={
        "stop_id": BigInteger,
        "stop_name": Text,
        "stop_lat": Float,
        "stop_lon": Float,
        "zone_id": BigInteger
    })


if __name__ == "__main__":
    main()
