import pandas as pd
import ssl
import datetime
from sqlalchemy import create_engine
from pathlib import Path
from urllib.error import URLError

csv_source_url = 'https://opendata.rhein-kreis-neuss.de/api/v2/catalog/datasets/rhein-kreis-neuss-flughafen-weltweit/exports/csv'
db_path = Path('airports.sqlite')

# Meaningful column names
# column_mapping = {
#     'column_1': 'ID',
#     'column_2': 'Airport_Name',
#     'column_3': 'City',
#     'column_4': 'Country',
#     'column_5': 'IATA',
#     'column_6': 'ICAO',
#     'column_7': 'Latitude',
#     'column_8': 'Longitude',
#     'column_9': 'Altitude',
#     'column_10': 'Timezone',
#     'column_11': 'DST',
#     'column_12': 'Tz_database_time_zone',
#     'geo_punkt': 'Geo_Point'
# }


def read_data(csv_source_url, db_path):
    try:
        data = pd.read_csv(csv_source_url, sep=";")
        store_data(data)
        print("Stored data without any issues")
    except URLError as e:
        if isinstance(e.reason, ssl.SSLError):
            # SSL Certificate no longer valid. Ignore SSL certificate verification and try again.
            ssl._create_default_https_context = ssl._create_unverified_context
            data = pd.read_csv(csv_source_url, sep=";")
            store_data(data)
            print("Stored data whilst ignoring SSL certificate verification")
        else:
            # If it's some other error, re-raise it
            raise
    except pd.errors.EmptyDataError:
        # If the file does not exist or is empty
        if not db_path.exists():
            raise ValueError("No data found and no database exists.")
        else:
            lastModificationTime = db_path.stat().st_mtime
            modification_date = datetime.datetime.fromtimestamp(lastModificationTime)
            if modification_date.year < datetime.datetime.now().year - 1:
                raise ValueError(
                    "[ERR] No data found ot source! Local database is older than 1 year! Please resolve the "
                    "issue!")
            else:
                print("[WARN] No data found at source, but a recent database exists.")


def store_data(data):
    """
    No error occurred, proceed to rename and store data
    Beware: Renaming happens in place!
    """
    #data.rename(columns=column_mapping, inplace=True)
    engine = create_engine(f'sqlite:///{db_path}')
    data.to_sql('airports', engine, if_exists='replace', index=False)


read_data(csv_source_url, db_path)
