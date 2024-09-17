'''
helper functions supporting knowledge_base API routes
'''
import copy

import nest_asyncio

import db.knowledge_base.mongo_helper as mongo
from db.knowledge_base.kb_config import KnowledgeBase
import db.app_logger as log

nest_asyncio.apply()

def get_all():
    return mongo.get_knowledge_bases()

def get_one(get_id):
    kb_config = mongo.get_knowledge_base(get_id)
    if kb_config:
        return kb_config

    return { "message": f"{get_id} does not exist" }

def create(client_config):
    if mongo.knowledge_base_name_taken(client_config['kb_name']):
        message = f"{client_config['kb_name']} already exists"
        return {"message": message}

    kb_config = create_kb_config(client_config)
    result = mongo.insert_knowledge_base(kb_config)
    kb_id = str(result.inserted_id)
    mongo.add_id_to_kb_config(kb_config["kb_name"], kb_id)

    log.info("knowledge base created: ", result)
    new_kb = mongo.get_knowledge_base(kb_id)
    return new_kb

def create_kb_config(client_config):
    kb_config = copy.copy(client_config)
    kb_config["splitter_config"] = str_to_nums(kb_config["splitter_config"])
    kb_config["files"] = []
    log.info("kb_config.py _create_kb_config: ", client_config, kb_config)
    return kb_config

async def upload_file(get_id, file):
    log.info("in route", file.filename)
    if not mongo.get_knowledge_base(get_id):
        return {"message": f"Knowledge base {get_id} doesn't exist"}

    if mongo.file_exists(get_id, file):
        return {"message": f"{file.filename} already in knowledge base"}

    kb = KnowledgeBase(get_id)
    log.info("in logic", file.filename)
    try:
        await kb.ingest_file(file)
        return {"message": f"{file.filename} uploaded"}
    except Exception as e:
        return {"message": f"Error: {e}"}

def delete(get_id):
    result = mongo.delete_knowledge_base(get_id)
    if result.deleted_count == 1:
        return {"message": f"{get_id} deleted"}

    return {"message": f"{get_id} does not exist"}


# config helpers to convert strings to numbers
def str_to_nums(config_dict):
    result = {}
    for key in config_dict:
        if is_int(config_dict[key]):
            result[key] = int(config_dict[key])
        elif is_float(config_dict[key]):
            result[key] = float(config_dict[key])
        else:
            result[key] = config_dict[key]

    return result

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
