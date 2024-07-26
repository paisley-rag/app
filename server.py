from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import app_logger as log
import shutil
import os
import use_s3
import load_vectors
# import lp_ingest
import simple_ingest
import evals
import nest_asyncio

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
    eval_table = evals.get_running_evals()
    return {"message": eval_table}

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

    # lp_ingest.ingest_file_to_docdb(file_location)
    log.info('starting simple_ingest')
    simple_ingest.ingest_file_to_docdb(file_location)
    log.info('finishing simple_ingest')

    return {"message": f"{file.filename} received"}

@app.post('/api/csv')
async def upload(file: UploadFile=File(...)):
    FILE_DIR = 'tmpfiles/csv'

    # write file to disk
    if not os.path.exists(f"./{FILE_DIR}"):
        os.makedirs(f"./{FILE_DIR}")

    file_location = f"./{FILE_DIR}/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    use_s3.ul_file(file.filename, dir=FILE_DIR)

    return {"message": f"{file.filename} received"}

class UserQuery(BaseModel):
    query: str


@app.post('/api/query')
async def post_query(query: UserQuery):
    print('user query: ', query)
    response = load_vectors.submit_query(query.query)
    # evals.store_running_eval_data(query.query, response)
    return { "type": "response", "body":response }


@app.post('/api/test')
async def test_query(query: UserQuery):
    log.debug("/api/test accessed", query, query.query)
    # print('user query: ', query.query)
    return { "type": "response", "body": query }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
