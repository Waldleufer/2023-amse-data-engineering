import pandas as pd
import time
from sqlalchemy import create_engine


def main():
    url = 'https://www-genesis.destatis.de/genesis/downloads/00/tables/46251-0021_00.csv'
    df = read_csv_with_retries(url)
    df = rename_and_filter_columns(df)
    df = assign_datatypes(df)
    df = validate_data(df)
    write_to_sqlite(df, 'cars.sqlite', 'cars')


def read_csv_with_retries(url, max_retries=5):
    """
    The encoding is set to 'iso-8859-1' to preserve German special characters
    Skip the first 6 and last 4 rows since they contain metadata
    Perform exponential back-off if unsuccessful for 4 additional times after the initial call
    """
    for attempt in range(max_retries):
        try:
            df = pd.read_csv(url, sep=';', skiprows=6, skipfooter=4, encoding='iso-8859-1', engine='python',
                             dtype={'Unnamed: 1': str})
            return df
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f'Attempt {attempt + 1} failed, retrying in {wait_time} seconds...')
                time.sleep(wait_time)
            else:
                raise Exception(f'Failed to fetch data after {max_retries} attempts. The last exception was: {str(e)}') from None


def rename_and_filter_columns(df):
    # Rename columns based on their index
    columns = df.columns.tolist()
    indices_to_rename = {
        0: 'date',
        1: 'CIN',
        2: 'name',
        12: 'petrol',
        22: 'diesel',
        32: 'gas',
        42: 'electro',
        52: 'hybrid',
        62: 'plugInHybrid',
        73: 'others'
    }
    for index, new_name in indices_to_rename.items():
        if index < len(columns):
            columns[index] = new_name
    df.columns = columns
    # Only keep required columns
    df = df[['date', 'CIN', 'name', 'petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']]
    return df


def assign_datatypes(df):
    df['date'] = df['date'].astype(str)
    df['CIN'] = df['CIN'].astype(str)
    df['name'] = df['name'].astype(str)

    for column in ['petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        df[column] = df[column].fillna(0).astype(int)
    return df


def validate_data(df):
    df = df[df['CIN'].apply(lambda x: isinstance(x, str) and len(x) == 5)]
    for column in ['petrol', 'diesel', 'gas', 'electro', 'hybrid', 'plugInHybrid', 'others']:
        df = df[df[column].apply(lambda x: x > 0)]
    return df


def write_to_sqlite(df, database_name, table_name):
    engine = create_engine(f'sqlite:///{database_name}')
    df.to_sql(table_name, engine, if_exists='replace', index=False)


if __name__ == '__main__':
    main()
