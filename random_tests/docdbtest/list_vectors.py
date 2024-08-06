# this mini program is to list the vectors within the documentDB instance that were written by llamaIndex
# Note:  the db and collection as named below - these can be changed when the vector_store is instantiated


import pymongo
import pprint
from dotenv import load_dotenv
import os

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
client = pymongo.MongoClient(mongo_uri)


db = client[os.environ["DOCDB_NAME"]]
collection = db[os.environ["DOCDB_COLLECTION"]]

for post in collection.find():
  pprint.pprint(post)


print('==========')
