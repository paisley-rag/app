import shutil
import os
import json

from fastapi import FastAPI, File, UploadFile, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import pymongo
from dotenv import load_dotenv

import app_logger as log
import use_s3
import evals
import pipeline
from kb_config import KnowledgeBase
import mongo_util as mutil
import config_util as cutil

# test if we need this w/n the server
nest_asyncio.apply()

load_dotenv(override=True)
MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]
CONFIG_PIPELINE_COL = os.environ["CONFIG_PIPELINE_COL"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

@app.get('/api')
async def root():
    log.info("server running")
    return {"message": "Server running"}


# knowledge base routes
@app.get("/api/knowledge-bases")
async def get_knowledge_bases():
    knowledge_bases = KnowledgeBase.get_knowledge_bases()
    return knowledge_bases

# consider adding id to the body of the request sent from the client
# to create a new knowledge base
# otherwise, we will use the kb_name prop to see if knowledge base exists
@app.post('/api/knowledge-bases')
async def create_kb(request: Request):
    body = await request.json()
    # ensure that the kb_name is unique
    if KnowledgeBase.exists(body["kb_name"]):
        message = f"{body['kb_name']} already exists"
    else:
        message = KnowledgeBase.create(body)

    return {"message": message}

@app.get("/api/knowledge-base/{id}")
async def get_knowledge_base(id: str):
    kb_config = KnowledgeBase.exists(id)
    if kb_config:
        return kb_config
    else:
        return { "message": f"{id} does not exist" }

# this route adds a file to a knowledge base
@app.post('/api/knowledge-bases/{id}/upload')
async def upload_file(id: str, file: UploadFile=File(...)):
    if KnowledgeBase.exists(id):
        kb = KnowledgeBase(id)
        kb.ingest_file(file)
        return {"message": f"{file.filename} uploaded"}
    else:
        return {"message": f"Knowledge base {id} doesn't exist"}

# pipeline routes
class UserQuery(BaseModel):
    query: str

class QueryBody(UserQuery):
    chatbot_id: str

@app.post('/api/query')
async def post_query(body: QueryBody):
    log.info('/api/query body received: ', body.query, body.chatbot_id)
    pipe = pipeline.Pipeline(body.chatbot_id)
    log.info('/api/query pipeline retrieved')
    response = pipe.query(body.query)
    evals.store_running_eval_data(body.chatbot_id, body.query, response)
    log.info('/api/query response:', response)
    return { "type": "response", "body": response }


@app.get('/api/chatbots')
async def get_chatbots():
    log.info('/api/chatbots loaded')
    results = mutil.get_all(CONFIG_DB, CONFIG_PIPELINE_COL, {}, { '_id': 0 })
    log.info('/api/chatbots results:', results)
    return json.dumps(results)


@app.get('/api/chatbots/{id}')
async def get_chatbot_id(id: str):
    results = mutil.get(CONFIG_DB, CONFIG_PIPELINE_COL, {"id": id}, {'_id': 0})
    log.info(f"/api/chatbots/{id}: ", results)
    if not results:
        return json.dumps({"message": "no chatbot configuration found"})

    return json.dumps(results)


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


@app.post('/api/chatbots')
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


@app.get('/api/history')
async def get_evals():
    data = evals.get_chat_history()
    return {"table_data": data}






@app.post('/api/test')
async def test_query(query: UserQuery):
    log.debug("/api/test accessed", query, query.query)
    return { "type": "response", "body": query }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
