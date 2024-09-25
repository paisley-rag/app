'''
Python script to drop many mongo dbs (e.g., from kb)
- used list_dbs.py to get list of dbs
- pasted those into dbs_to_drop
- then run script
'''
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
client = pymongo.MongoClient(os.getenv('MONGO_URI'))

dbs_to_drop = []

for db in dbs_to_drop:
    print(db)
    client.drop_database(db)

client.close()
