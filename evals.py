# RAGAs dependencies
from datasets import Dataset 
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness, context_precision, context_recall, context_entity_recall, answer_similarity, answer_correctness

import eval_pg_utils as pg
import eval_utils as utils

from server import UserQuery, post_query

import app_logger as log

# called within the server /api/query route
def store_running_eval_data(query, response):
    context, output = utils.extract_from_response(response)
    evaluate_and_store_running_entry(query, context, output)


# takes query/context/output, scores on 'answer_relevancy' and 'faithfulness'
# using RAGAs, inserts data into 'running_evals' table
def evaluate_and_store_running_entry(chatbot_id, query, context, output):
    data_samples = {
        'question': [query],
        'answer': [output],
        'contexts' : [[context]], # currently the context is globbed into one string, can change that later
    }

    dataset = Dataset.from_dict(data_samples)

    score = evaluate(dataset, metrics=[answer_relevancy, faithfulness])
    score = utils.change_nans_to_zeros(score)

    entry = {
        'chatbot_id': chatbot_id,
        'input': query,
        'context': context,
        'output': output,
        'scores': score
    }

    pg.insert_dict_in(entry, table='running_evals')


async def evaluate_benchmark_data():
    table_data = get_benchmark_data()
    data_list = utils.values_only(table_data)
    print(data_list)

    for entry in data_list:

        user_query = UserQuery(query=entry['input'])
        response = await post_query(user_query)
        
        context, output = utils.extract_from_response(response)
        entry['context'] = context
        entry['output'] = output
        evaluate_and_store_benchmark_data_entry(entry)

def evaluate_and_store_benchmark_data_entry(entry):
    data_samples = {
        'question': [entry['query']],
        'answer': [entry['output']],
        'contexts' : [[entry['context']]], # currently the context is globbed into one string, can change that later
        'ground_truth': [entry['ground_truth']]
    }

    dataset = Dataset.from_dict(data_samples)

    score = evaluate(dataset, metrics=[
        answer_relevancy,
        faithfulness,
        context_precision,
        context_recall,
        context_entity_recall,
        answer_similarity,
        answer_correctness
    ])

    score = utils.change_nans_to_zeros(score)

    scored_entry = entry.copy()
    scored_entry['scores'] = score

    pg.insert_scored_benchmark_data(scored_entry)

def get_chat_history(chatbot_id):
    data = pg.get_data_from('chat_history')
    data = utils.filter_by_chatbot(data, chatbot_id)
    return data

def get_benchmark_data():
    data = pg.get_data_from('benchmark_data')
    return data

def get_benchmark_scores():
    data = pg.get_data_from('scored_benchmark_data')
    return data

