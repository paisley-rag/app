from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from dotenv import load_dotenv

import app_logger as log
import pipeline.routes

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

@app.get('/api')
async def root():
    log.info("server running")
    return {"message": "Server running"}

# pipeline routes

@app.post('/api/query')
async def post_query(body: pipeline.routes.QueryBody):
    return pipeline.routes.post_query(body)


@app.get('/api/chatbots')
async def get_chatbots():
    return pipeline.routes.get_chatbots()


@app.get('/api/chatbots/{id}')
async def get_chatbot_id(id: str):
    return pipeline.routes.get_chatbots_id(id)



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
    return await pipeline.routes.post_chatbots(request)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
