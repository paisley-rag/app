import os

import pymongo
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path=".env.testing")

MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_KB_COL = os.environ["CONFIG_KB_COL"]

kb_names = []
def drop_all_knowledge_bases():
    print(f"Dropping all knowledge bases in {CONFIG_DB}")
    pymongo.MongoClient(MONGO_URI).drop_database(CONFIG_DB)

def remove_kb_files(kb_names: list):
    mongo_client = pymongo.MongoClient(MONGO_URI)

    for kb_name in kb_names:
        mongo_client.drop_database(kb_name)

drop_all_knowledge_bases()


