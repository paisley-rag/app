import math

import db.app_logger as log

def values_only(table_data):
    return [data[1] for data in table_data]

def extract_from_response(response):
    # creates context using 'text' from each 'node' in response's 'source_nodes'. also deletes any instances of '\n'
    source_nodes = response.source_nodes
    context_list = [source_node.node.text.replace('\n', '') for source_node in source_nodes] 
    context = '\n\n'.join(context_list)

    output = response.response

    return [context, output]

def change_nans_to_zeros(score):
    # sometimes when the context and answer really don't match RAGAs gives a 'NaN' faithfulness answer score, which I'll replace with 0.0 for now
    # otherwise it causes issues when trying to insert into the psql table
    for key in score:
        if isinstance(score[key], float) and math.isnan(score[key]):
            score[key] = 0.0
    
    return score
