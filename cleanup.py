import os

import pymongo
from dotenv import load_dotenv

load_dotenv(override=True, dotenv_path=".env.testing")


MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_KB_COL = os.environ["CONFIG_KB_COL"]
print(f"CONFIG_DB: {CONFIG_DB}")

kb_names = ["Sentence", "Semantic", "Markdown"]
def drop_all_knowledge_bases():
    print(f"Dropping all knowledge bases in {CONFIG_DB}")
    client = pymongo.MongoClient(MONGO_URI)
    client.drop_database(CONFIG_DB)
    client.close()


def remove_kb_files(kb_names: list):
    client = pymongo.MongoClient(MONGO_URI)

    for kb_name in kb_names:
        client.drop_database(kb_name)
    
    client.close()

drop_all_knowledge_bases()
remove_kb_files(kb_names)



