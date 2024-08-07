import os

import pymongo
from dotenv import load_dotenv
# import app_logger as log

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]


def get(db_name, db_collection, query=None, projection=None):
    mongo = pymongo.MongoClient(mongo_uri)
    result = mongo[db_name][db_collection].find_one(query, projection)
    mongo.close()
    return result


# used in /api/chatbots route
def get_all(db_name, db_collection, query=None, projection=None):
    mongo = pymongo.MongoClient(mongo_uri)
    results = mongo[db_name][db_collection].find(query, projection)
    results = list(results)
    mongo.close()
    # ar = []
    # for result in results:
    #     ar.append(result)
    return results


def insert_one(db_name, db_collection, doc):
    mongo = pymongo.MongoClient(mongo_uri)
    result = mongo[db_name][db_collection].insert_one(doc)
    mongo.close()
    return result



# unused
# def update(db_name, db_collection, filter=None, newObj=None):
#     mongo[db_name][db_collection].UpdateOne(filter, newObj)
#     log.info(f"mongo_util.py update:  {db_name} {db_collection} {filter} {newObj}")
