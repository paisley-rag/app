from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric 

from dotenv import load_dotenv
load_dotenv()

def get_scores(query, context, output):
    test_case = LLMTestCase(
        input=query, 
        retrieval_context=[context],
        actual_output=output
    )

    metrics = [
        ("answer_relevancy", AnswerRelevancyMetric()),
        ("faithfulness", FaithfulnessMetric()),
        ("context_relevancy", ContextualRelevancyMetric())
    ]
    
    scores = {}
    for name, metric in metrics:
        metric.measure(test_case)
        scores[name] = metric.score
    
    # print('SCORES:', scores)
    return scores
