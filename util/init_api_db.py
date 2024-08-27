'''

Utility file to populate new db instance with valid API key

'''

import hashlib
import random
import pprint


'''

Mongo utility to populate docDb with valid API keys

'''

import os
import pymongo
from dotenv import load_dotenv

load_dotenv(override=True)

MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_API_COL = os.environ["CONFIG_API_COL"]

def insert(new_obj):
    mongo = pymongo.MongoClient(MONGO_URI)
    result = mongo[CONFIG_DB][CONFIG_API_COL].insert_one(new_obj)
    mongo.close()
    return result

###

'''

Utility functions to generate API_KEYS

'''

def digest(string):
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def generate_key():
    seed = str(random.randint(1000000,9999999))
    return digest(seed)


'''

Initial auth data for DocDB

Notes:
- admin pw was "pizza"; initial api_key was previously generated and used for testing
- bob pw was "specialpassword"
- pw hashes were previously generated using argon2-cffi library (new standard over and above bcrypt)

'''

api_db_data = {
    "id0": {
        "name": digest('admin'),
        "pw": "$argon2id$v=19$m=65536,t=3,p=4$94csP7TfX/0v7Ogvj13lzw$oyGbZPx2TVnywdX8AxhWREM8dJf1diOkYZW+DnU5viQ",
        "api_key": "272de67e6ab46cd6c09cd5149e7e5889"
    },
    "id1": {
        "name": digest('bob'),
        "pw": "$argon2id$v=19$m=65536,t=3,p=4$3KdzGOGDCC+HD25As7f5yA$sl4bP3DMd7AgFvk4SOkOSZUipuk3Q6j41+tyWlvsGXs",
        "api_key": generate_key()
    }
}

'''

Populate docDB with auth data

'''

def insert_db(new_obj):
    for key in new_obj:
        insert(new_obj[key])
    print('Object below inserted to docDB')
    pprint.pp(new_obj)


def write_api_key_to_env(api_data, id_string):
    api_key = api_data[id_string]["api_key"]
    print('API AUTH KEY ADDED TO .ENV:', api_key)
    env_path = os.path.expanduser("~/db/.env")
    with open(env_path, "a") as env_file:
        env_file.write(f"\nVITE_PAISLEY_API_KEY={api_key}\n")

if __name__ == "__main__":
    insert_db(api_db_data)
    write_api_key_to_env(api_db_data, "id1")