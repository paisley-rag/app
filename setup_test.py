# helper scripts to populate test kbs
import os

import pymongo
from dotenv import load_dotenv

import hybridSearch.search as search

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
mongo = pymongo.MongoClient(mongo_uri)


# kb1
kb1_file_path = './tmpfiles/AsyncJS.md'
search.keyword_write('kb1', kb1_file_path)
search.vector_write('kb1', kb1_file_path)

#kb2
kb2_file_path = './tmpfiles/cpumemory.pdf'
search.hybrid_write('kb2', kb2_file_path)

#kb3
kb3_file_path = './tmpfiles/newfile.txt'
search.hybrid_write('kb3', kb3_file_path)


# config db setup

kb_config1 = {
    'id': 'kb1',
    'name': 'AsyncJS',
    'files': [{ 'filename': './tmpfiles/AsyncJS.md'}],
    'ingest': {
        'method': 'simple_ingest',
        'splitter': {
            'type': 'sentence',
            'chunk_size': '',
            'chunk_overlap': '',
            'separator': '',
        },
    },
    'embedding_model': 'gpt-3.5-turbo',
    'vector_store': {
        'name': 'idstring',
        'collection': 'vector_index',
    },
    'keyword_store': {
        'name': 'idstring',
        'collections': ['docstore/ref_doc_info', 'docstore/data', 'docstore/metadata']
    }
}

kb_config2 = kb_config1.copy()
kb_config2['id'] = 'kb2'
kb_config2['name'] = 'cpumemory'
kb_config2['files'] = [{ 'filename': './tmpfiles/cpumemory.pdf'}],


kb_config3 = kb_config1.copy()
kb_config3['id'] = 'kb3'
kb_config3['name'] = 'newfile'
kb_config3['files'] = [{ 'filename': './tmpfiles/newfile.txt'}],


config_db = mongo[ os.environ["CONFIG_DB"] ]
config_kb_col = config_db[ os.environ["CONFIG_KB_COL"] ]
config_kb_col.insert_one(kb_config1)
config_kb_col.insert_one(kb_config2)
config_kb_col.insert_one(kb_config3)




# Pipeline config

pipeline_config1 = {
    'id': 'pipeline1',
    'name': 'pipelineConfigName',
    'knowledgebases': ['kb1', 'kb2', 'kb3'],
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

pipeline_config2 = pipeline_config1.copy()
pipeline_config2['id'] = 'pipeline2'
pipeline_config2['name'] = 'kb1 only (async)'
pipeline_config2['knowledgebases'] = ['kb1']


pipeline_config3 = pipeline_config1.copy()
pipeline_config3['id'] = 'pipeline3'
pipeline_config3['name'] = 'kb2 only (cpumemory)'
pipeline_config3['knowledgebases'] = ['kb2']

pipeline_config4 = pipeline_config1.copy()
pipeline_config4['id'] = 'pipeline4'
pipeline_config4['name'] = 'kb1 (async) and kb2 (cpumemory)'
pipeline_config4['knowledgebases'] = ['kb2', 'kb1']

config_pipeline_col = config_db[ os.environ["CONFIG_PIPELINE_COL"] ]
config_pipeline_col.insert_one(pipeline_config1)
config_pipeline_col.insert_one(pipeline_config2)
config_pipeline_col.insert_one(pipeline_config3)
config_pipeline_col.insert_one(pipeline_config4)


