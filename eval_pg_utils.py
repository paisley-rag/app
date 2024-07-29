import psycopg2
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
    insert_query = "INSERT INTO {table} (data) VALUES (%s)".format(table=table)
    cursor.execute(insert_query, (json_data,))
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
    cursor.execute(f"SELECT * FROM {table}")
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
        
        # Prepare the SQL query
        insert_query = f"INSERT INTO benchmark_data (data) VALUES (%s)"

        # Insert each row as a JSONB object
        for row in csvreader:
            json_data = Json(row)
            cursor.execute(insert_query, (json_data,))

    log.info("csv benchmark data successfully imported into table 'benchmark_data'.")
    # Commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()

def printable_table(table_data):
    log.info("displaying table:")

    if not table_data:
        log.info("No data to display.")
        return

    data_list = values_only(table_data)
    
    # Get all unique keys from all dictionaries
    all_keys = set()
    for item in data_list:
        all_keys.update(item.keys())
    
    # Convert to sorted list for consistent column order
    headers = sorted(all_keys)

    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for item in data_list:
        for i, key in enumerate(headers):
            value = str(item.get(key, ''))
            col_widths[i] = max(col_widths[i], len(max(value.split(), key=len, default='')))

    # Adjust column widths to fit within 100 characters
    total_width = sum(col_widths) + len(headers) * 3 + 1
    if total_width > 100:
        excess = total_width - 100
        for i in range(len(col_widths)):
            if col_widths[i] > 10:
                reduction = min(excess, col_widths[i] - 10)
                col_widths[i] -= reduction
                excess -= reduction
            if excess == 0:
                break

    # Create the table
    table = []
    
    # Add header
    header_row = '|' + '|'.join(f' {h:<{w}} ' for h, w in zip(headers, col_widths)) + '|'
    table.append(header_row)
    table.append('+' + '+'.join('-' * (w + 2) for w in col_widths) + '+')

    # Add data rows
    for item in data_list:
        row_data = []
        for key, width in zip(headers, col_widths):
            value = str(item.get(key, ''))
            wrapped = textwrap.wrap(value, width)
            row_data.append(wrapped or [''])
        
        max_lines = max(len(cell) for cell in row_data)
        for i in range(max_lines):
            row = '|'
            for j, cell in enumerate(row_data):
                if i < len(cell):
                    row += f' {cell[i]:<{col_widths[j]}} |'
                else:
                    row += ' ' * (col_widths[j] + 2) + '|'
            table.append(row)
        table.append('+' + '+'.join('-' * (w + 2) for w in col_widths) + '+')

    return '\n'.join(table)

