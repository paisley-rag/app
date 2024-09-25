'''
helper functions supporting knowledge_base API routes
'''
import copy
import db.app_logger as log

def create_kb_config(client_config):
    kb_config = copy.copy(client_config)
    kb_config["splitter_config"] = str_to_nums(kb_config["splitter_config"])
    kb_config["files"] = []
    log.info("kb_config.py _create_kb_config: ", client_config, kb_config)
    return kb_config

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
