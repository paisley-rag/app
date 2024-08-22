import db.evals.eval_pg_utils as pg
import db.evals.eval_utils as utils
# import db.evals.ragas_evaluate as ragas
# import db.evals.deepeval_evaluate as deepeval
import db.evals.all_metrics as all_metrics

# from server import UserQuery, post_query

import db.app_logger as log

# called within the server /api/query route
# def store_running_eval_data(chatbot_id, query, response):
#     context, output = utils.extract_from_response(response)
#     evaluate_and_store_running_entry(chatbot_id, query, context, output)

# takes query/context/output, scores on 'answer_relevancy' and 'faithfulness'
# using RAGAs, inserts data into 'chat_history' table
def evaluate_and_store_running_entry(chatbot_id, query, context, output):
    scores = all_metrics.all_scores(query, context, output)

    entry = {
        'chatbot_id': chatbot_id,
        'input': query,
        'context': context,
        'output': output,
        'scores': scores
    }

    pg.insert_dict_in(entry, table='chat_history')

def get_chat_history():
    data = pg.get_data_from('chat_history')
    
    score_names = utils.get_score_names()
    
    json_data_list = []

    for tuple in data:
        json_data = {
            'pg_id': tuple[0],
            'chatbot_id': tuple[2]['chatbot_id'],
            'time': tuple[1],
            'input': tuple[2]['input'],
            'output': tuple[2]['output'],
            'context': tuple[2]['context'],
        }

        for score in score_names:
            json_data[score] = tuple[2]['scores'].get(score, None)

        json_data_list.append(json_data)

    return json_data_list


# async def evaluate_benchmark_data():
#     table_data = get_benchmark_data()
#     data_list = utils.values_only(table_data)
#     print(data_list)

#     for entry in data_list:

#         user_query = UserQuery(query=entry['input'])
#         response = await post_query(user_query)
        
#         context, output = utils.extract_from_response(response)
#         entry['context'] = context
#         entry['output'] = output
#         evaluate_and_store_benchmark_data_entry(entry)
# def evaluate_and_store_benchmark_data_entry(entry):
#     data_samples = {
#         'question': [entry['query']],
#         'answer': [entry['output']],
#         'contexts' : [[entry['context']]], # currently the context is globbed into one string, can change that later
#         'ground_truth': [entry['ground_truth']]
#     }

#     dataset = Dataset.from_dict(data_samples)

#     score = evaluate(dataset, metrics=[
#         answer_relevancy,
#         faithfulness,
#         context_precision,
#         context_recall,
#         context_entity_recall,
#         answer_similarity,
#         answer_correctness
#     ])

#     score = utils.change_nans_to_zeros(score)

#     scored_entry = entry.copy()
#     scored_entry['scores'] = score

#     pg.insert_scored_benchmark_data(scored_entry)
# def get_benchmark_data():
#     data = pg.get_data_from('benchmark_data')
#     return data
# def get_benchmark_scores():
#     data = pg.get_data_from('scored_benchmark_data')
#     return data

