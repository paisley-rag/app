import os

import pymongo
from dotenv import load_dotenv

load_dotenv(override=True)

MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_API_COL = os.environ["CONFIG_API_COL"]

def key_exists(api_key):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_API_COL].find_one(
        { "api_key": api_key },
        { "_id": 0 }
    )
    mongo.close()
    if result:
        return True
    else:
        return False
    

def insert(new_obj):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_API_COL].insert_one(new_obj)
    mongo.close()
    return result