import os
import pymongo

MONGO_URI = os.environ["MONGO_URI"]
KB_CONFIG_DOCDB = os.environ["KB_CONFIG_DOCDB"]
KB_CONFIG_COLLECTION_DOCDB = os.environ["KB_CONFIG_COLLECTION_DOCDB"]
PYMONGO_CLIENT = pymongo.MongoClient(MONGO_URI)

def connect(db, collection):
    try:
        db = PYMONGO_CLIENT[db]
        collection = db[collection]
        return collection
    except Exception as e:
        print("An error occurred while connecting to the database:", e)
        return None
    
def connect_to_kb_config():
    return connect(KB_CONFIG_DOCDB, KB_CONFIG_COLLECTION_DOCDB)

def client():
    return PYMONGO_CLIENT