import os

import pymongo
from dotenv import load_dotenv

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

def delete_pipeline(id):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].delete_one(
        { "id": id }
    )
    mongo.close()
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

def update_pipeline(id, new_config):
    old_config = get_one_pipeline(id)
    updates = compare_configs(old_config, new_config)

    if updates:
        mongo = pymongo.MongoClient(MONGO_URI)
        result = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].update_one(
            { "id": id },
            { "$set": updates }
        )
        mongo.close()
    
    return get_one_pipeline(id)

def compare_configs(old_config, new_config):
    updates = {}
    for key in new_config:
        if new_config[key] != old_config[key]:
            updates[key] = new_config[key]
    return updates

# used in pipeline_class
def nodes_in_keyword(kb_id):
    mongo = pymongo.MongoClient(MONGO_URI)

    results = mongo[kb_id]['docstore/ref_doc_info'].find( 
        {},
        { '_id': 0 }
    )
    results = list(results)
    mongo.close()

    return len(results)