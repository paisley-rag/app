from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

import db.app_logger as log
import db.util.use_s3
import db.evals.evals as evals
import db.pipeline.query as pq
import db.knowledge_base.routes as kb

from db.routers import chatbots

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

app.include_router(chatbots.router)


@app.get('/api')
async def root():
    log.info("server running")
    return {"message": "Server running"}

# knowledge base routes

# get all knowledge bases
@app.get("/api/knowledge-bases")
async def get_knowledge_bases():
    return kb.get_all()

# create a knowledge base
@app.post('/api/knowledge-bases')
async def create_knowledge_base(request: Request):
    client_config = await request.json()
    return kb.create(client_config)

# get one knowledge base's configuration details
@app.get("/api/knowledge-bases/{id}")
async def get_knowledge_base(id: str):
    return kb.get_one(id)

@app.delete("/api/knowledge-bases/{id}/delete")
async def delete_knowledge_base(id: str):
    return kb.delete(id)

# add a file to a knowledge base
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
    evals.store_running_eval_data(
        body.chatbot_id,
        body.query,
        response
    )
    return response

@app.get('/api/history')
async def get_evals():
    data = evals.get_chat_history()
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
