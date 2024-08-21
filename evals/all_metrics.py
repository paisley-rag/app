import os
import importlib
import json

def all_scores(query, context, output):
    eval_config_path = os.path.join(os.path.dirname(__file__), 'eval_config.json')
    with open(eval_config_path, 'r') as f:
        eval_config = json.load(f)
    
    if eval_config.get('evaluation_toggle', 'false').lower() == 'false':
        return {}


    # Get all filenames within the 'metrics' directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    metrics_dir = os.path.join(script_dir, 'metrics')
    files = [f for f in os.listdir(metrics_dir) if f.endswith('.py')]

    scores = {}

    for file in files:
        module_name = 'db.evals.metrics.' + file.replace('.py', '')
        print('IMPORTING:', module_name)
        module = importlib.import_module(module_name)
        if hasattr(module, 'get_scores'):
            scores.update(module.get_scores(query, context, output))

    return scores
    # SCORES: {'score1': 111, 'score2': 2, 'score3': 3}