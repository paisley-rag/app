"""
Mini program to list data in mongo/docDB
"""

import os
import sys
import pprint

import pymongo
from dotenv import load_dotenv

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
client = pymongo.MongoClient(mongo_uri)

print(sys.argv[1:2])

db_name = sys.argv[1:2][0] if sys.argv[1:2] else os.environ["DOCDB_NAME"]
db_collection = sys.argv[2:3][0] if sys.argv[2:3] else os.environ["DOCDB_COLLECTION"]

print('db_name ', db_name, db_collection)
db = client[db_name]
collection = db[db_collection]

for post in collection.find():
    pprint.pprint(post)


print('==========')

print(f"collections in db: {db_name}")
print(client[db_name].list_collection_names())
