"""
Mini program to list vectors within mongo/docDB
"""

# import pprint
import os

import pymongo
from dotenv import load_dotenv

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
client = pymongo.MongoClient(mongo_uri)

print(client.list_database_names())
