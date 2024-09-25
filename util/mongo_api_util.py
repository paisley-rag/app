'''
Helper utility to check if api key exists within config_api collection
- currently unused (using JWT auth instead of API key authentication)
'''
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
    return bool(result)
