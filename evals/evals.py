'''
primary evals functions
'''
import db.evals.eval_pg_utils as pg
import db.evals.eval_utils as utils
from db.evals import all_metrics

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

    for pair in data:
        json_data = {
            'pg_id': pair[0],
            'chatbot_id': pair[2]['chatbot_id'],
            'time': pair[1],
            'input': pair[2]['input'],
            'output': pair[2]['output'],
            'context': pair[2]['context'],
        }

        for score in score_names:
            json_data[score] = pair[2]['scores'].get(score, None)

        json_data_list.append(json_data)

    return json_data_list
