import shutil
import os

from fastapi import FastAPI, File, UploadFile, Request
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio

import app_logger as log
import use_s3
# import lp_ingest
import simple_ingest
import evals

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

class UserQuery(BaseModel):
    query: str

@app.get('/api')
async def root():
    log.info("server running")
    return {"message": "Server running"}








# QUERY/CHAT ROUTES

# api route for document uploads to add to document collection
# TESTED, WORKING 7/29/24
# required key/values for Postman:
    # file => upload file via Postman
    # filename => file name
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
    #     log.info('starting simple_ingest')
    #     simple_ingest.ingest_file_to_docdb(file_location)
    #     log.info('finishing simple_ingest')

    return {"message": f"{file.filename} received"}
@app.get('/api/evals')
async def get_evals():
    eval_table = evals.get_evals()
    return {"message": eval_table}

# this route creates a new knowledge base
@app.post('/api/create_kb')
async def create_kb(request: Request):
    body = await request.json()
    # ensure that the kb_name is unique
    if KnowledgeBase.exists(body["kb_name"]):
        message = f"{body['kb_name']} already exists"
        status = 400
    else:
        message = KnowledgeBase.create(body)
        status = 201

    return {"message": message, "status_code": status}

@app.get("/api/{kb_name}/files")
async def get_kb_files(kb_name: str):
    if KnowledgeBase.exists(kb_name):
        kb = KnowledgeBase(kb_name)
        log.info(kb)
        files = kb.get_files(kb_name)
        log.info(files)
        return {
            "files": files,
            "status_code": 200
        }
    
    else:
        return {
            "message": f"{kb_name} does not exist",
            "status_code": 404
        }

# this route adds a file to a knowledge base
@app.post('/api/{kb_name}/upload_file')
async def upload(kb_name: str, file: UploadFile=File(...)):
    if KnowledgeBase.exists(kb_name):
        kb = KnowledgeBase(kb_name)
        kb.ingest_file(file)
        return {
                "message": f"{file.filename} received",
                "status_code": 201
                }
    else:
        return {
                "message": f"Knowledge base {kb_name} doesn't exist",
                "status_code": 404
                }


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


@app.post('/api/test')
async def test_query(body: QueryBody):
    log.debug("/api/test accessed", body)
    return { "type": "response", "query": body.query }


# pipeline query with side effects of the input/context/output being evaluated and stored in chat history
# TESTED, WORKING 7/29/24
# same Postman requirements as '/api/query'
@app.post('/api/chat')
async def post_chat(query: UserQuery):
    response = await post_query(query)
    evals.store_chat_eval_data(query.query, response)

# route for observing pipeline input/output history + associated evaluation scores
# TESTED, WORKING 7/29/24
@app.get('/api/history')
async def get_evals():
    data = evals.get_chat_history()
    return {"table_data": data}





# BENCHMARK ROUTES

# benchmark api route for uploading of csv data for use as benchmark data
# TESTED, WORKING 7/29/24
@app.post('/api/benchmark/upload')
async def benchmark_upload(file: UploadFile=File(...)):
    FILE_DIR = 'tmpfiles'

    # write file to disk
    if not os.path.exists(f"./{FILE_DIR}"):
        os.makedirs(f"./{FILE_DIR}")

    file_location = f"./{FILE_DIR}/{file.filename}"

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    use_s3.ul_file(file.filename, dir=FILE_DIR)

    # import csv to postgres benchmark_data table
    evals.pg.import_csv_benchmark_data(file_location)

    return {"message": f"{file.filename} received"}

# benchmark api route for batch-evaluating stored benchmark data
@app.post('/api/benchmark/evaluate')
async def benchmark_evaluate():
    try:
        await evals.evaluate_benchmark_data()
        return {"message": "Benchmark data evaluated successfully", "status_code": 200}
    except Exception as e:
        print(f"Error evaluating benchmark data: {str(e)}")
        return {"message": "Failed to evaluate benchmark data", "status_code": 500}

# benchmark api route for examining evaluation results of benchmark data
@app.get('/api/benchmark/results')
async def benchmark_results():
    data = evals.get_benchmark_scores()
    return {"table_data": data}


# benchmark api route for viewing uploaded benchmark data
@app.get('/api/benchmark/view')
async def benchmark_data():
    data = evals.get_benchmark_data()
    return {"table_data": data}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
