import shutil
import os

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

import app_logger as log
import use_s3
import simple_ingest
import pipeline

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


@app.post('/api/upload')
async def upload(file: UploadFile=File(...)):
    FILE_DIR = 'tmpfiles'

    # write file to disk
    if not os.path.exists(f"./{FILE_DIR}"):
        os.makedirs(f"./{FILE_DIR}")

    file_location = f"./{FILE_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    use_s3.ul_file(file.filename, dir=FILE_DIR)

    log.info('starting simple_ingest')
    simple_ingest.ingest_file_to_docdb(file_location)
    log.info('finishing simple_ingest')

    return {"message": f"{file.filename} received"}



# updated

class QueryBody(BaseModel):
    query: str
    pipeline_config: str


@app.post('/api/query')
async def post_query(body: QueryBody):
    log.info('/api/query body received: ', body.query, body.pipeline_config)
    pipe = pipeline.Pipeline(body.pipeline_config)
    log.info('/api/query pipeline retrieved')
    response = pipe.query(body.query)
    log.info('/api/query response:', response)
    return { "type": "response", "body": response }
    # return { "type": "response", "body":response }


@app.post('/api/test')
async def test_query(body: QueryBody):
    log.debug("/api/test accessed", body)
    return { "type": "response", "query": body.query }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
