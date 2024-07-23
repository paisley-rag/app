# RAGAs dependencies
from datasets import Dataset 
import os
from ragas import evaluate
from ragas.metrics import answer_relevancy

# DB dependencies
import psycopg2

from dotenv import load_dotenv

load_dotenv()

def connect_to_db():
    try:
        conn = psycopg2.connect(
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST", "127.0.0.1"),
            port=os.getenv("PG_PORT", "5432"),
            database=os.getenv("PG_DATABASE", "paisley_evals")
        )
        print("Connection to the database has been established.")
        return conn
    except Exception as e:
        print("An error occurred while connecting to the database:", e)
        return None


def run_evals(query=None, output=None, context=None):
    data_samples = {
        'question': [query],
        'answer': [output],
        'contexts' : [[context]],
    }

    dataset = Dataset.from_dict(data_samples)

    score = evaluate(dataset, metrics=[answer_relevancy])
    answer_relevancy_score = score['answer_relevancy']
    print('score', answer_relevancy_score)
    
    store_to_db(query, output, context, answer_relevancy_score)

def store_to_db(query, output, context, answer_relevancy_score):
    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO evals (query, output, context, answer_relevancy_score)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = cursor.fetchall()
    print("Existing tables in the database:", [table[0] for table in tables])
    
    cursor.execute(insert_query, (query, output, context, answer_relevancy_score))
    conn.commit()
    cursor.close()
    conn.close()

def get_evals():
    conn = connect_to_db()
    if conn is None:
        return
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evals")
    records = cursor.fetchall()
    print(records)
    return records

# run_evals(
#     query='When was the second super bowl?', 
#     output='The first superbowl was held on January 15, 1967', 
#     context='The first superbowl was held on January 15, 1967'
# )
# 
# get_evals()
