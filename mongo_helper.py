import os
import pymongo

MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_KB_COL = os.environ["CONFIG_KB_COL"]
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
    return connect(CONFIG_DB, CONFIG_KB_COL)

def client():
    return PYMONGO_CLIENT

# write helper to retrieve knowledge base id from name
def get_kb_id(kb_name):
    kb_col = connect_to_kb_config()
    kb = kb_col.find_one({"kb_name": kb_name})
    return kb["_id"]