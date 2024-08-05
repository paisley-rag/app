import os
import json

from fastapi import Request
from pydantic import BaseModel
from dotenv import load_dotenv

import app_logger as log
import pipeline.pipeline_class
import pipeline.mongo_util as mutil
import pipeline.config_util as cutil

load_dotenv(override=True)
MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_PIPELINE_COL = os.environ["CONFIG_PIPELINE_COL"]

class UserQuery(BaseModel):
    query: str

class QueryBody(UserQuery):
    chatbot_id: str

def post_query(body: QueryBody):
    log.info('/api/query body received: ', body.query, body.chatbot_id)
    pipe = pipeline.pipeline_class.Pipeline(body.chatbot_id)
    log.info('/api/query pipeline retrieved')
    response = pipe.query(body.query)
    log.info('/api/query response:', response)
    return { "type": "response", "body": response }

def get_chatbots():
    log.info('/api/chatbots loaded')
    results = mutil.get_all(CONFIG_DB, CONFIG_PIPELINE_COL, {}, { '_id': 0 })
    log.info('/api/chatbots results:', results)
    return json.dumps(results)


def get_chatbots_id(id):
    results = mutil.get(CONFIG_DB, CONFIG_PIPELINE_COL, {"id": id}, {'_id': 0})
    log.info(f"/api/chatbots/{id}: ", results)
    if not results:
        return json.dumps({"message": "no chatbot configuration found"})

    return json.dumps(results)

async def post_chatbots(request: Request):
    body = await request.json()
    log.info(f"/api/chatbots POST body: ", body)
    pipeline_obj = cutil.ui_to_pipeline(json.dumps(body))

    mutil.insert_one(CONFIG_DB, CONFIG_PIPELINE_COL, pipeline_obj)
    # insert_one seems to include the '_id' property which cannot be serialized by json.dumps
    del pipeline_obj['_id']

    pipeline_json = json.dumps(pipeline_obj)
    log.debug(f"/api/chatbots POST: pipeline_obj, pipeline_json", pipeline_obj, pipeline_json)
    return pipeline_json



    # JSON Shape from UI
    # {
    #       "id": "test1",
    #       "name": "test1",
    #       "knowledge_bases": ["giraffes"],
    #       "generative_model": "gpt-4-o",
    #       "similarity": {
    #             "on": "True",
    #             "cutoff": 0.5
    #           },
    #       "colbert_rerank": {
    #             "on": "True",
    #             "top_n": 0.4
    #           },
    #       "long_contet_reorder": "True",
    #       "prompt": "hello"
    # }

