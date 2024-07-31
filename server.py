from fastapi import FastAPI, File, UploadFile, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import app_logger as log
import shutil
import os
import use_s3
import load_vectors
# import lp_ingest
# import simple_ingest
import evals
import nest_asyncio
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
    log.info("server running")
    return {"message": "Server running"}

@app.get('/api/evals')
async def get_evals():
    eval_table = evals.get_evals()
    return {"message": eval_table}

# this route creates a new knowledge base
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

@app.get("/api/{kb_name}")
async def get_kb_files(kb_name: str):
    if KnowledgeBase.exists(kb_name):
        kb = KnowledgeBase(kb_name)
        log.info(kb)
        files = kb.get_files()
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

    kb = KnowledgeBase(kb_name)
    kb.ingest_file(file)
    
    return {"message": f"{file.filename} received"}

class UserQuery(BaseModel):
    query: str


@app.post('/api/query')
async def post_query(query: UserQuery):
    print('user query: ', query)
    response = load_vectors.submit_query(query.query)
    evals.store_eval_data(query.query, response)
    return { "type": "response", "body":response }


@app.post('/api/test')
async def test_query(query: UserQuery):
    log.debug("/api/test accessed", query, query.query)
    # print('user query: ', query.query)
    return { "type": "response", "body": query }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
