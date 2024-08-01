from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

import app_logger as log
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


@app.get("/api/knowledge-bases")
async def get_knowledge_bases():
    knowledge_bases = KnowledgeBase.get_knowledge_bases()
    return knowledge_bases

    # return KnowledgeBase.get_knowledge_base(id)

@app.post('/api/knowledge-bases')
async def create_kb(request: Request):
    body = await request.json()
    # ensure that the kb_name is unique
    if KnowledgeBase.exists(body["id"]):
        message = f"{body['id']} already exists"
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
async def upload(id: str, file: UploadFile=File(...)):
    if KnowledgeBase.exists(id):
        kb = KnowledgeBase(id)
        kb.ingest_file(file)
        return {"message": f"{file.filename} uploaded"}
    else:
        return {
                "message": f"Knowledge base {id} doesn't exist"}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')


# @app.get("/api/{kb_name}/files")
# async def get_kb_files(kb_name: str):
#     if KnowledgeBase.exists(kb_name):
#         kb = KnowledgeBase(kb_name)
#         log.info(kb)
#         files = kb.get_files(kb_name)
#         log.info(files)
#         return {
#             "files": files,
#             "status_code": 200
#         }

#     else:
#         return {
#             "message": f"{kb_name} does not exist",
#             "status_code": 404
#         }