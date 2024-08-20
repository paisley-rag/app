from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ContextualRelevancyMetric 

from dotenv import load_dotenv
load_dotenv()

async def get_scores(query, context, output):
    test_case = LLMTestCase(
        input=query, 
        retrieval_context=context,
        actual_output=output
    )

    metrics = [
        # AnswerRelevancyMetric(threshold=0),
        # FaithfulnessMetric(threshold=0),
        ContextualRelevancyMetric(threshold=0),
    ]
    
    scores = evaluate(
        [test_case],
        metrics,
        print_results=False,
        verbose_mode=False,
    )
    
    data = scores[0].metrics_data
    final_scores = {}
    for datum in data:
        name = datum.name.lower().replace(' ', '_')
        final_scores[name] = datum.score

    return final_scores
