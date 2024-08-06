from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from dotenv import load_dotenv

import app_logger as log
import pipeline.query
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


@app.post('/api/query')
async def post_query(body: pipeline.query.QueryBody):
    return pipeline.query.post_query(body)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
