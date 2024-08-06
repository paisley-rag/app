# import shutil
# import os

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from dotenv import load_dotenv

import app_logger as log
# import util.use_s3
# import evals
import pipeline.query
from kb_config import KnowledgeBase

from routers import chatbots

# test if we need this w/n the server
nest_asyncio.apply()

load_dotenv(override=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.include_router(chatbots.router)


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


# query route
@app.post('/api/query')
async def post_query(body: pipeline.query.QueryBody):
    return pipeline.query.post_query(body)



# evals routes

# @app.get('/api/evals')
# async def get_evals():
#     eval_table = evals.get_running_evals()
#     return {"message": eval_table}
# 
# @app.post('/api/csv')
# async def upload_csv(file: UploadFile=File(...)):
#     FILE_DIR = 'tmpfiles/csv'
# 
#     # write file to disk
#     if not os.path.exists(f"./{FILE_DIR}"):
#         os.makedirs(f"./{FILE_DIR}")
# 
#     file_location = f"./{FILE_DIR}/{file.filename}"
#     with open(file_location, "wb+") as file_object:
#         shutil.copyfileobj(file.file, file_object)
# 
#     util.use_s3.ul_file(file.filename, dir=FILE_DIR)
# 
#     return {"message": f"{file.filename} received"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
