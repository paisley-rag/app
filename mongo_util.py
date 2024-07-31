import os

import pymongo
from dotenv import load_dotenv
import app_logger as log

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
mongo = pymongo.MongoClient(mongo_uri)

def get(db_name, db_collection, query=None):
    return mongo[db_name][db_collection].find_one(query)

def update(db_name, db_collection, filter=None, newObj=None):
    mongo[db_name][db_collection].UpdateOne(filter, newObj)
    log.info(f"mongo_util.py update:  {db_name} {db_collection} {filter} {newObj}")
