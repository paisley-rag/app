import shutil
import os
import json

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
import pymongo
from dotenv import load_dotenv

import app_logger as log
import use_s3
from knowledge_base.kb_config import KnowledgeBase

nest_asyncio.apply()

# env = os.getenv("ENV")
# print(env)
# if env == 'testing':
#     load_dotenv(override=True, dotenv_path='.env.testing')
# else:
#     load_dotenv(override=True)

# MONGO_URI = os.environ["MONGO_URI"]
# CONFIG_DB = os.environ["CONFIG_DB"]
# # print(CONFIG_DB)
# CONFIG_PIPELINE_COL = os.environ["CONFIG_PIPELINE_COL"]

print("Starting server")
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
    log.info("in route", file.filename)
    if KnowledgeBase.exists(id):
        kb = KnowledgeBase(id)
        log.info("in logic", file.filename)
        try:
            await kb.ingest_file(file)
            return {"message": f"{file.filename} uploaded"}
        except Exception as e:
            return {"message": f"Error: {e}"}
    else:
        return {"message": f"Knowledge base {id} doesn't exist"}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')