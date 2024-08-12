import os

import pymongo
from dotenv import load_dotenv
# import app_logger as log

load_dotenv(override=True)

MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_PIPELINE_COL = os.environ["CONFIG_PIPELINE_COL"]

def get_one_pipeline(id):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].find_one(
        {"id": id},
        {'_id': 0}
    )
    mongo.close()
    return result


# used in /api/chatbots route
def get_all_pipelines():
    mongo = pymongo.MongoClient(MONGO_URI)
    results = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].find( 
        {},
        { '_id': 0 }
    )
    results = list(results)
    mongo.close()

    return results

def pipeline_name_taken(name):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].find_one(
        { "name": name },
        { '_id': 0 }
    )
    return result


def insert_pipeline(doc):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].insert_one(doc)
    mongo.close()
    return result

def add_id_to_pipeline_config(name, inserted_id):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].update_one(
        { "name": name },
        { "$set": { "id": inserted_id } }
    )
    return result

# def get_knowledge_base(id):
    # mongo = pymongo.MongoClient(MONGO_URI)
    # result = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].find_one(

# unused
# def update(db_name, db_collection, filter=None, newObj=None):
#     mongo[db_name][db_collection].UpdateOne(filter, newObj)
#     log.info(f"mongo_util.py update:  {db_name} {db_collection} {filter} {newObj}")


# {
#     "name": "test1",
#     "knowledge_bases": [
#         "66b57127c01ea14ceaeeda98"
#     ],
#     "generative_model": "gpt-4-o",
#     "postprocessing": {
#         "similarity": {
#             "on": "True",
#             "similarity_cutoff": 0.0
#         },
#         "colbert_rerank": {
#             "on": "True",
#             "top_n": 0.0
#         },
#         "long_context_reorder": {
#             "on": "True"
#         },
#     },
#     "prompt": {
#         "on": "True",
#         "template_str": "Hello"
#     },
# }