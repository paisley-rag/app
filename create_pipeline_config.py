import os
import sys

import pymongo
from dotenv import load_dotenv

# import hybridSearch.search as search

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
mongo = pymongo.MongoClient(mongo_uri)

config_name = sys.argv[1:2][0] if sys.argv[1:2] else None
kb_id = sys.argv[2:3][0] if sys.argv[2:3] else None

if not config_name or not kb_id:
    print('please enter [config_name] and [kb_id] as arguments')
else:
    pipeline_config = {
        'id': config_name,
        'name': config_name,
        'knowledgebases': [kb_id],
        'retrieval': {
            'vector': 'llm_model_name',
        },
        'postprocessing': {
            'similarity': {
                'on': False,
                'similarity_cutoff': 0.7
            },
            'colbertRerank': {
                'on': False,
                'top_n': 5
            },
            'longContextReorder': {
                'on': True,
            }
        },
        'generative_model': 'gpt-3.5-turbo',
        'prompt': {
            'on': True,
            'template_str': 'answer the question - {query_str} - in French'
        }
    }



    config_db = mongo[ os.environ["CONFIG_DB"] ]
    config_pipeline_col = config_db[ os.environ["CONFIG_PIPELINE_COL"] ]
    config_pipeline_col.insert_one(pipeline_config)
