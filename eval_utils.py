import math

import app_logger as log

def extract_from_response(response):
    # creates context using 'text' from each 'node' in response's 'source_nodes'. also deletes any instances of '\n'
    log.debug('RESPONSE IS:', response)
    log.debug('RESPONSE TYPE IS:', type(response))
    source_nodes = response.body.source_nodes
    context_list = [source_node.node.text.replace('\n', '') for source_node in source_nodes] 
    context = '\n\n'.join(context_list)

    output = response.body.response

    return [context, output]

def change_nans_to_zeros(score):
    # sometimes when the context and answer really don't match RAGAs gives a 'NaN' faithfulness answer score, which I'll replace with 0.0 for now
    # otherwise it causes issues when trying to insert into the psql table
    for key in score:
        if isinstance(score[key], float) and math.isnan(score[key]):
            score[key] = 0.0
    
    return score