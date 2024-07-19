
# RAGAs dependencies
from datasets import Dataset 
import os
from ragas import evaluate
from ragas.metrics import answer_relevancy


# DB dependencies
import os
import psycopg2
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy


import psycopg2

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
    conn = psycopg2.connect(
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host="127.0.0.1",
        port="5432",
        database="evals"
    )
    cursor = conn.cursor()
    insert_query = """
    INSERT INTO evals (query, output, context, answer_relevancy_score)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (query, output, context, answer_relevancy_score))
    conn.commit()
    cursor.close()
    conn.close()

def get_evals():
    conn = psycopg2.connect(
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host="127.0.0.1",
        port="5432",
        database="evals"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM evals")
    records = cursor.fetchall()
    print(records)
    return records

run_evals(
    query='When was the second super bowl?', 
    output='The first superbowl was held on January 15, 1967', 
    context='The first superbowl was held on January 15, 1967'
)

get_evals()