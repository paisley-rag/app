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
    
    relevancy_metric = AnswerRelevancyMetric()
    faithfulness_metric = FaithfulnessMetric()
    context_relevancy_metric = ContextualRelevancyMetric()

    relevancy_metric.measure(test_case)
    faithfulness_metric.measure(test_case)
    context_relevancy_metric.measure(test_case)

    scores = {
        "answer_relevancy": relevancy_metric.score,
        "faithfulness": faithfulness_metric.score,
        "context_relevancy": context_relevancy_metric.score,
    }
    
    # print('SCORES:', scores)
    return scores
