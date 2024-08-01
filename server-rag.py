import shutil
import os
import json

from fastapi import FastAPI, File, UploadFile, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

import app_logger as log
import use_s3
import simple_ingest
import pipeline
import mongo_util as mutil
import config_util as cutil

nest_asyncio.apply()

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


@app.post('/api/upload')
async def upload(file: UploadFile=File(...)):
    FILE_DIR = 'tmpfiles'

    # write file to disk
    if not os.path.exists(f"./{FILE_DIR}"):
        os.makedirs(f"./{FILE_DIR}")

    file_location = f"./{FILE_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    use_s3.ul_file(file.filename, dir=FILE_DIR)

    log.info('starting simple_ingest')
    simple_ingest.ingest_file_to_docdb(file_location)
    log.info('finishing simple_ingest')

    return {"message": f"{file.filename} received"}

# updated Aug 1, 2024

class QueryBody(BaseModel):
    query: str
    chatbot_id: str


@app.post('/api/query')
async def post_query(body: QueryBody):
    log.info('/api/query body received: ', body.query, body.chatbot_id)
    pipe = pipeline.Pipeline(body.chatbot_id)
    log.info('/api/query pipeline retrieved')
    response = pipe.query(body.query)
    log.info('/api/query response:', response)
    return { "type": "response", "body": response }


# new routes for UI


@app.get('/api/chatbots')
async def get_chatbots():
    log.info('/api/chatbots loaded')
    results = mutil.get_all('configs', 'config_pipeline', {}, { '_id': 0 })
    log.info('/api/chatbots results:', results)
    return json.dumps(results)



@app.get('/api/chatbots/{id}')
async def get_chatbot_id(id: str):
    results = mutil.get('configs', 'config_pipeline', {"id": id}, {'_id': 0})
    log.info(f"/api/chatbots/{id}: ", results)
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
    #       "long_context_reorder": "True",
    #       "prompt": "hello"
    # }


@app.post('/api/chatbots')
async def post_chatbots(request: Request):
    body = await request.json()
    log.info(f"/api/chatbots POST body: ", body)
    pipeline_obj = cutil.ui_to_pipeline(json.dumps(body))
    pipeline_json = json.dumps(pipeline_obj)
    log.info(f"/api/chatbots POST: pipeline_obj", pipeline_obj, pipeline_json)
    return pipeline_json




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
