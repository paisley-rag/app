from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

import db.app_logger as log
import db.evals.evals as evals
import db.pipeline.query as pq

from db.routers import chatbots
from db.routers import api_auth
from db.routers import knowledge_bases
from db.util.auth import check_key

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

app.include_router(
    api_auth.router,
    dependencies=[Depends(check_key)]
)

app.include_router(
    chatbots.router,
    dependencies=[Depends(check_key)]
)

app.include_router(
    knowledge_bases.router,
    dependencies=[Depends(check_key)]
)

@app.get('/api')
async def root():
    log.info("server running")
    return {"message": "Server running"}



# query route
@app.post('/api/query')
async def post_query(body: pq.QueryBody, auth: bool = Depends(check_key)):
    response = pq.post_query(body)
    evals.store_running_eval_data(
        body.chatbot_id,
        body.query,
        response
    )
    return response

@app.get('/api/history')
async def get_evals(auth: bool = Depends(check_key)):
    data = evals.get_chat_history()
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
