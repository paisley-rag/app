import os

import pymongo
from dotenv import load_dotenv
import app_logger as log

env = os.getenv("ENV")
if env == 'testing':
    log.info("Testing environment")
    load_dotenv(override=True, dotenv_path='.env.testing')
else:
    load_dotenv(override=True)

MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_KB_COL = os.environ["CONFIG_KB_COL"]

def get(db_name, db_collection, query=None, projection=None):
    mongo = pymongo.MongoClient(MONGO_URI)
    return mongo[db_name][db_collection].find_one(query, projection)

def get_all(db_name, db_collection, query=None, projection=None):
    mongo = pymongo.MongoClient(MONGO_URI)
    results = mongo[db_name][db_collection].find(query, projection)
    ar = []
    for result in results:
        ar.append(result)
    return ar

def insert_one(db_name, db_collection, doc):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[db_name][db_collection].insert_one(doc)
    return result

def get_knowledge_bases():
    return get_all(CONFIG_DB, CONFIG_KB_COL,{}, {"_id": 0})

def get_knowledge_base(kb_name):
    return get(
        CONFIG_DB,
        CONFIG_KB_COL,
        {"kb_name": kb_name},
        {"_id": 0}
    )

def insert_knowledge_base(kb_config):
    return insert_one(CONFIG_DB, CONFIG_KB_COL, kb_config)

def add_file_metadata_to_kb(kb_name, file_metadata):
    mongo = pymongo.MongoClient(MONGO_URI)
    mongo[CONFIG_DB][CONFIG_KB_COL].update_one(
        { "kb_name": kb_name },
            { "$push": { "files": file_metadata } }
    )
