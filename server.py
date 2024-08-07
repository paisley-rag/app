"""

Main back-end server file 
- run with `python server.py`
  (fastapi syntax does not seem to work with asyncio)

"""
# import shutil
# import os

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from dotenv import load_dotenv

import db.app_logger as log
import db.util.use_s3
import db.evals as evals
import db.pipeline.query as pq
import db.knowledge_base.routes as kb

from db.routers import chatbots

# test if we need this w/n the server
nest_asyncio.apply()

# load_dotenv(override=True)

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
    return kb.get_all()

# consider adding id to the body of the request sent from the client
# to create a new knowledge base
# otherwise, we will use the kb_name prop to see if knowledge base exists
@app.post('/api/knowledge-bases')
async def create_knowledge_base(request: Request):
    client_config = await request.json()
    return kb.create(client_config)

@app.get("/api/knowledge-base/{id}")
async def get_knowledge_base(id: str):
    return kb.get_one(id)

# this route adds a file to a knowledge base
@app.post('/api/knowledge-bases/{id}/upload')
async def upload_file(id: str, file: UploadFile=File(...)):
    try:
        return await kb.upload_file(id, file)
        
    except Exception as e:
        return {"message": f"Error: {e}"}

# query route
@app.post('/api/query')
async def post_query(body: pq.QueryBody):
    response = pq.post_query(body)
    # add evals stuff here
    #     evals.store_running_eval_data(
    #         body.chatbot_id,
    #         body.query,
    #         response
    #     )
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
