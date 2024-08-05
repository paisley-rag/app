"""
Mini program to list the vectors within mongo/docDB
"""

# import pprint
import os
import sys

import pymongo
from dotenv import load_dotenv

load_dotenv(override=True)

mongo_uri = os.environ["MONGO_URI"]
client = pymongo.MongoClient(mongo_uri)


print(sys.argv[1:2])

db_name = sys.argv[1:2][0] if sys.argv[1:2] else None

if db_name:
    client.drop_database(db_name)
    print(f"{db_name} dropped")
else:
    print('No db_name provided, nothing dropped')
