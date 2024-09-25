'''
postgres / rds helper functions for evals
'''
import csv
import os
import json

import psycopg2
from psycopg2.extras import Json
import db.app_logger as log

from dotenv import load_dotenv
load_dotenv()

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

def insert_chat_history(obj):
    insert_dict_in(obj, 'chat_history')

def insert_benchmark_data(obj):
    insert_dict_in(obj, 'benchmark_data')

def insert_scored_benchmark_data(obj):
    insert_dict_in(obj, 'scored_benchmark_data')

def insert_dict_in(obj, table=''):
    log.info(f"inserting data into {table}")
    json_data = json.dumps(obj)
    conn = connect_to_db()
    if conn is None:
        log.info(f"table {table} not found.")
        return

    cursor = conn.cursor()
    insert_query = f"INSERT INTO {table} (data) VALUES (%s)"
    cursor.execute(insert_query, (json_data,))
    conn.commit()
    cursor.close()
    conn.close()
    log.info(f"JSONB data stored in '{table}' successfully.")

def get_data_from(table=''):
    log.info(f"retrieving data from {table}")
    conn = connect_to_db()
    if conn is None:
        log.info(f"table {table} not found.")
        return None

    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    records = cursor.fetchall()

    log.info("data retrieved.")
    return records

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
    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)

        # Clear the existing data from the benchmark_data table
        cursor.execute("DELETE FROM benchmark_data")
        log.info("Existing data in 'benchmark_data' table has been cleared.")

        # Prepare the SQL query
        insert_query = "INSERT INTO golden_dataset (data) VALUES (%s)"

        # Insert each row as a JSONB object
        for row in csvreader:
            json_data = Json(row)
            cursor.execute(insert_query, (json_data,))

    # Commit the changes and close the connection
    log.info("csv benchmark data successfully imported into table 'benchmark_data'.")
    conn.commit()
    cursor.close()
    conn.close()
