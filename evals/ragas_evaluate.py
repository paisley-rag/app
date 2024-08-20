# RAGAs dependencies
from datasets import Dataset 
from ragas import evaluate
from ragas.metrics import answer_relevancy, faithfulness

import db.evals.eval_utils as utils

def get_scores(query, context, output):
    data_samples = {
        'question': [query],
        'answer': [output],
        'contexts' : [context], # currently the context is globbed into one string, can change that later
    }

    dataset = Dataset.from_dict(data_samples)
    scores = evaluate(dataset, metrics=[answer_relevancy, faithfulness])
    scores = utils.change_nans_to_zeros(scores)

    # shape of scores dict:
    # scores = {
    #     "answer_relevancy": 0.67,
    #     "faithfulness": 0.5,
    # }

    return scores