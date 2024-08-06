import json

# import unittest
import db.pipeline.config_util as cutil

# class TestConfigUtil(unittest.TestCase):

def test_1():
    request = {
        'id': 'string',
        'name': 'string',
        'knowledge_bases': ['string'],
        'generative_model': 'string',
        'similarity': {
            'on': True,
            'cutoff': 0.3,
        },
        'colbert_rerank': {
            'on': True,
            'top_n': 0.4,
        },
        'long_context_reorder': True,
        'prompt': 'string',
    }

    output = cutil.ui_to_pipeline(json.dumps(request))
    assert "colbertRerank" in output['postprocessing']

# if __name__ == '__main__':
#     unittest.main()
