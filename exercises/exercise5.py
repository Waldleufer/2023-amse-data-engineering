import ssl
import urllib.request
import zipfile
import pandas as pd
from sqlalchemy import create_engine, BigInteger, Text, Float


def download_file(url, filename):
    # SSL Certificate no longer valid. Ignore SSL certificate verification
    ssl._create_default_https_context = ssl._create_unverified_context
    urllib.request.urlretrieve(url, filename)


def extract_file(zipfile_name, file_to_extract):
    with zipfile.ZipFile(zipfile_name, 'r') as zip_ref:
        zip_ref.extract(file_to_extract)


def load_and_filter_data(filename, columns, filter_column, filter_value):
    df = pd.read_csv(filename, usecols=columns)
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

    download_file(gtfs_url, gtfs_zipfile_name)
    extract_file(gtfs_zipfile_name, stops_filename)
    df_stops = load_and_filter_data(stops_filename, stops_columns, zone_id_column, target_zone_id)
    df_stops_validated = validate_data(df_stops, coordinate_columns)
    write_to_sqlite(df_stops_validated, sqlite_db_name, sqlite_table_name)


if __name__ == "__main__":
    main()
