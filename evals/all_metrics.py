import os
import importlib

def all_scores(query, context, output):
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