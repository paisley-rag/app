import shutil
import os

from fastapi import FastAPI, File, UploadFile, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

import app_logger as log
import use_s3
import evals
import pipeline
from kb_config import KnowledgeBase

# test if we need this w/n the server
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

@app.get('/api/evals')
async def get_evals():
    eval_table = evals.get_running_evals()
    return {"message": eval_table}


@app.post('/api/create_kb')
async def create_kb(request: Request):
    body = await request.json()
    # ensure that the kb_name is unique
    if KnowledgeBase.exists(body["kb_name"]):
        message = f"{body['kb_name']} already exists"
        status = 400
    else:
        message = KnowledgeBase.create(body)
        status = 201

    return {"message": message, "status_code": status}

@app.get("/api/{kb_name}/files")
async def get_kb_files(kb_name: str):
    if KnowledgeBase.exists(kb_name):
        kb = KnowledgeBase(kb_name)
        log.info(kb)
        files = kb.get_files(kb_name)
        log.info(files)
        return {
            "files": files,
            "status_code": 200
        }

    else:
        return {
            "message": f"{kb_name} does not exist",
            "status_code": 404
        }

# this route adds a file to a knowledge base
@app.post('/api/{kb_name}/upload_file')
async def upload(kb_name: str, file: UploadFile=File(...)):
    if KnowledgeBase.exists(kb_name):
        kb = KnowledgeBase(kb_name)
        kb.ingest_file(file)
        return {
                "message": f"{file.filename} received",
                "status_code": 201
                }
    else:
        return {
                "message": f"Knowledge base {kb_name} doesn't exist",
                "status_code": 404
                }


class UserQuery(BaseModel):
    query: str

class QueryBody(UserQuery):
    pipeline_config: str


@app.post('/api/query')
async def post_query(body: QueryBody):
    log.info('/api/query body received: ', body.query, body.pipeline_config)
    pipe = pipeline.Pipeline(body.pipeline_config)
    log.info('/api/query pipeline retrieved')
    response = pipe.query(body.query)
    log.info('/api/query response:', response)
    return { "type": "response", "body": response }


@app.post('/api/test')
async def test_query(body: QueryBody):
    log.debug("/api/test accessed", body)
    return { "type": "response", "query": body.query }


# QUERY/CHAT ROUTES


@app.post('/api/csv')
async def upload(file: UploadFile=File(...)):
    FILE_DIR = 'tmpfiles/csv'

    # write file to disk
    if not os.path.exists(f"./{FILE_DIR}"):
        os.makedirs(f"./{FILE_DIR}")

    file_location = f"./{FILE_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    use_s3.ul_file(file.filename, dir=FILE_DIR)

    return {"message": f"{file.filename} received"}

class UserQuery(BaseModel):
    query: str


@app.post('/api/query')
async def post_query(query: UserQuery):
    print('user query: ', query)
    response = load_vectors.submit_query(query.query)
    evals.store_running_eval_data(query.query, response)
    return { "type": "response", "body":response }


@app.post('/api/test')
async def test_query(query: UserQuery):
    log.debug("/api/test accessed", query, query.query)
    # print('user query: ', query.query)
    return { "type": "response", "body": query }



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
