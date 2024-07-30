# RAGAs dependencies
from datasets import Dataset 
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness, context_precision, context_recall, context_entity_recall, answer_similarity, answer_correctness

import eval_pg_utils as pg
import eval_utils as utils
import eval_test_utils as test

from server import post_query

import app_logger as log

# called within the server /api/query route
def store_chat_eval_data(query, response):
    context, output = utils.extract_from_response(response)
    evaluate_and_store_chat_entry(query, context, output)

# takes query/context/output, scores on 'answer_relevancy' and 'faithfulness'
# using RAGAs, inserts data into 'chat_history' table
def evaluate_and_store_chat_entry(query, context, output):
    data_samples = {
        'question': [query],
        'answer': [output],
        'contexts' : [[context]], # currently the context is globbed into one string, can change that later
    }

    dataset = Dataset.from_dict(data_samples)

    score = evaluate(dataset, metrics=[answer_relevancy, faithfulness])
    score = utils.change_nans_to_zeros(score)

    entry = {
        'input': query,
        'context': context,
        'output': output,
        'scores': score
    }

    pg.insert_dict_in(entry, table='chat_history')

from server import UserQuery

async def evaluate_benchmark_data():
    table_data = pg.get_data_from('benchmark_data')
    data_list = pg.values_only(table_data)
    print(data_list)

    for entry in data_list:
        print('THIS ENTRY IS:', entry)

        user_query = UserQuery(query=entry['input'])
        response = await post_query(user_query)

        print('RESPONSE BODY IS:', response)
        context, output = utils.extract_from_response(response)
        entry['context'] = context
        entry['output'] = output
        print('WITH OUTPUT AND CONTEXT, THIS ENTRY IS NOW:', entry)
        evaluate_and_store_benchmark_data_entry(entry)

def evaluate_and_store_benchmark_data_entry(entry):
    log.debug('ENTRY TYPE:', type(entry))
    log.debug('ENTRY KEYS:', entry.keys())
    data_samples = {
        'question': [entry['input']],
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
    print('SCORED ENTRY IS:', scored_entry)

    pg.insert_dict_in(scored_entry, table='scored_benchmark_data')

def get_chat_history():
    data = pg.get_data_from('chat_history')
    # print(pg.printable_table(data))
    return data

def get_benchmark_data():
    data = pg.get_data_from('benchmark_data')
    # print(pg.printable_table(data))
    return data

def get_benchmark_scores():
    data = pg.get_data_from('scored_benchmark_data')
    # print(pg.printable_table(data))
    return data

# if __name__ == "__main__":
    # evaluate_and_store_chat_entry('this is a query', 'this was the context', 'and we got this for output')
    # get_chat_history()
    # pg.import_csv_benchmark_data('./tmpfiles/strawberries_bananas.csv')
    # evaluate_benchmark_data()
    # pg.print_table(pg.get_data_from('scored_benchmark_data'))
  