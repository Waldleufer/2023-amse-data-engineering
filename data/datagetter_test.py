import os
import sqlite3
from datagetter import execute_pipeline


def test_execute_pipeline():
    # Delete the database if it exists
    if os.path.exists("preprocessed-data.sqlite"):
        os.remove("preprocessed-data.sqlite")

    # Run the pipeline
    execute_pipeline()

    # Verify that the database file was created
    assert os.path.exists("preprocessed-data.sqlite"), "Database file was not created"

    # Verify that the correct tables were created in the database
    conn = sqlite3.connect('preprocessed-data.sqlite')
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()

    # Check if the tuples ('TPZ_data',), ('EmZ_data',) and ('bikes_data',) exist in the tables list
    assert ('TPZ_data',) in tables, "TPZ_data table was not created in the database"
    assert ('EmZ_data',) in tables, "EmZ_data table was not created in the database"
    assert ('bikes_data',) in tables, "bikes_data table was not created in the database"

    print("Test execution completed without any errors.")


if __name__ == '__main__':
    test_execute_pipeline()
