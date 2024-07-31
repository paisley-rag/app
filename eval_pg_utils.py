import psycopg2
from psycopg2 import sql
from psycopg2.extras import Json
import csv
import os
import json
import textwrap

import app_logger as log

from dotenv import load_dotenv
load_dotenv(override=True)

def connect_to_db():
    try:
        conn = psycopg2.connect(
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST", "127.0.0.1"),
            port=os.getenv("PG_PORT", "5432"),
            database=os.getenv("PG_DATABASE")
        )
        log.info(f"Connection to the database '{os.getenv('PG_DATABASE')}' has been established.")
        return conn
    except Exception as e:
        log.info("An error occurred while connecting to the database:", e)
        return None
    
def insert_dict_in(dict, table=''):
    log.info(f"inserting data into {table}")
    json_data = json.dumps(dict)
    conn = connect_to_db()
    if conn is None:
        log.info(f"table {table} not found.")
        return
    cursor = conn.cursor()
    insert_query = "INSERT INTO %(table)s (data) VALUES (%(data)s)"
    cursor.execute(insert_query, { 'table': table, 'data': json_data })
    conn.commit()
    cursor.close()
    conn.close()
    print(f"JSONB data stored in '{table}' successfully.")

def get_data_from(table=''):
    log.info(f"retrieving data from {table}")
    conn = connect_to_db()
    if conn is None:
        log.info(f"table {table} not found.")
        return
    cursor = conn.cursor()
    query = "SELECT * FROM %s"
    cursor.execute(query, (table))
    records = cursor.fetchall()
    
    log.info("data retrieved.")
    return records

def values_only(table_data):
    return [data[1] for data in table_data]

def import_csv_benchmark_data(csv_file_path):
    log.info('Importing csv file...')
    log.info(f"Current working directory: {os.getcwd()}")

    # Print the absolute path
    log.info(f"Attempting to open file: {os.path.abspath(csv_file_path)}")

    if not os.path.exists(csv_file_path):
        log.info(f"Error: File not found: {csv_file_path}")
        return

    # Connect to the PostgreSQL database
    conn = connect_to_db()
    cursor = conn.cursor()

    # Read the CSV file
    with open(csv_file_path, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        
        # Clear the existing data from the benchmark_data table
        clear_query = "DELETE FROM benchmark_data"
        cursor.execute(clear_query)
        print("Existing data in 'benchmark_data' table has been cleared.")
        log.info("Existing data in 'benchmark_data' table has been cleared.")

        # Prepare the SQL query
        insert_query = "INSERT INTO benchmark_data (data) VALUES (%s)"

        # Insert each row as a JSONB object
        for row in csvreader:
            json_data = Json(row)
            cursor.execute(insert_query, (json_data,))

    log.info("csv benchmark data successfully imported into table 'benchmark_data'.")
    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()
