import os

import pymongo
from dotenv import load_dotenv
import db.app_logger as log

env = os.getenv("ENV")
if env == 'testing':
    log.info("Testing environment")
    load_dotenv(override=True, dotenv_path='.env.testing')
else:
    load_dotenv(override=True)

MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_PIPELINE_COL = os.environ["CONFIG_PIPELINE_COL"]
CONFIG_KB_COL = os.environ["CONFIG_KB_COL"]

def get(db_name, db_collection, query=None, projection=None):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[db_name][db_collection].find_one(query, projection)
    mongo.close()
    return result

def get_all(db_name, db_collection, query=None, projection=None):
    mongo = pymongo.MongoClient(MONGO_URI)
    print("config db:", CONFIG_DB)
    results = mongo[db_name][db_collection].find(query, projection)
    results = list(results)
    mongo.close()
    return results

# def insert_one(doc):
#     mongo = pymongo.MongoClient(MONGO_URI)
#     result = mongo[CONFIG_DB][CONFIG_KB_COL].insert_one(doc)
#     mongo.close()
#     return result

def get_knowledge_bases():
    return get_all(CONFIG_DB, CONFIG_KB_COL,{}, {"_id": 0})

def knowledge_base_name_taken(kb_name):
    return get(
        CONFIG_DB,
        CONFIG_KB_COL,
        {"kb_name": kb_name},
        {"_id": 0}
    )

def get_knowledge_base(id):
    return get(
        CONFIG_DB,
        CONFIG_KB_COL,
        {"id": id},
        {"_id": 0}
    )

def insert_knowledge_base(kb_config):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_KB_COL].insert_one(kb_config)
    mongo.close()
    return result

def add_file_metadata_to_kb(kb_name, file_metadata):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_KB_COL].update_one(
        { "kb_name": kb_name },
            { "$push": { "files": file_metadata } }
    )
    mongo.close()
    log.info(f"add_file_metadata_to_kb: {result}")

def file_exists(id, file):
    kb = get_knowledge_base(id)
    if kb:
        for f in kb["files"]:
            if (
                f["file_name"] == file.filename and
                f["size"] == file.size and
                f["content_type"] == file.headers["content-type"]
                ):
                return True
    return False

def add_id_to_kb_config(kb_name, kb_id):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_KB_COL].update_one(
        { "kb_name": kb_name },
        { "$set": { "id": kb_id } }
    )
    mongo.close()
    log.info(f"add_id_to_kb_config: {result}")

def get_kb_id(kb_name):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_KB_COL].find_one(
        {"kb_name": kb_name}
    )
    # print("result:", result)
    # print("result id:", result["_id"])
    print("result id string:", str(result["_id"]))
    # print("type of result id string:", type(str(result["_id"])))
    if result:
        return str(result["_id"])
    else:
        return None
    
def delete_knowledge_base(id):
    mongo = pymongo.MongoClient(MONGO_URI)
    kb_result = mongo[CONFIG_DB][CONFIG_KB_COL].delete_one({"id": id})
    pipeline_result = remove_kb_from_pipeline(id)
    mongo.close()

    return kb_result

def remove_kb_from_pipeline(kb_id):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_PIPELINE_COL].update_many(
        {},
        { "$pull": { "knowledge_bases": kb_id } }
    )
    log.info(f"remove_kb_from_pipeline: {result}")
    mongo.close()
    return result
    

# get_kb_id("Sentence Split")
