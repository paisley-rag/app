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

class UserQuery(BaseModel):
    query: str

@app.get('/api')
async def root():
    log.info("server running")
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
    log.info('starting simple_ingest')
    simple_ingest.ingest_file_to_docdb(file_location)
    log.info('finishing simple_ingest')

    return {"message": f"{file.filename} received"}

# simple pipeline query with no side effects
# TESTED, WORKING 7/29/24
# required body for Postman
    # body -> raw -> json
    # {
    #     "query": "how tall are banana trees"
    # }
@app.post('/api/query')
async def post_query(query: UserQuery):
    # print('user query: ', query)
    response = load_vectors.submit_query(query.query)
    return { "type": "response", "body":response }

# pipeline query with side effects of the input/context/output being evaluated and stored in chat history
# TESTED, WORKING 7/29/24
# same Postman requirements as '/api/query'
@app.post('/api/chat')
async def post_chat(query: UserQuery):
    response = await post_query(query)
    evals.store_running_eval_data(query.query, response)

# route for observing pipeline input/output history + associated evaluation scores
# TESTED, WORKING 7/29/24
@app.get('/api/history')
async def get_evals():
    data = evals.get_running_evals()
    return {"table_data": data}





# BENCHMARK ROUTES

# benchmark api route for uploading of csv data for use as benchmark data
# TESTED, WORKING 7/29/24
@app.post('/api/benchmark/upload')
async def upload(file: UploadFile=File(...)):
    FILE_DIR = 'tmpfiles'

    # write file to disk
    if not os.path.exists(f"./{FILE_DIR}"):
        os.makedirs(f"./{FILE_DIR}")

    file_location = f"./{FILE_DIR}/{file.filename}"

    # import csv to postgres benchmark_data table
    evals.pg.import_csv_benchmark_data(file_location)

    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)

    use_s3.ul_file(file.filename, dir=FILE_DIR)

    return {"message": f"{file.filename} received"}

# benchmark api route for batch-evaluating stored benchmark data
@app.post('/api/benchmark/evaluate')
async def benchmark_evaluate():
    await evals.evaluate_benchmark_data()
    # try:
    #     await evals.evaluate_benchmark_data()
    #     return {"message": "Benchmark data evaluated successfully", "status_code": 200}
    # except Exception as e:
    #     print(f"Error evaluating benchmark data: {str(e)}")
    #     return {"message": "Failed to evaluate benchmark data", "status_code": 500}

# benchmark api route for examining evaluation results of benchmark data
@app.get('/api/benchmark/results')
async def benchmark_results():
    data = evals.get_benchmark_scores()
    return {"table_data": data}





# HOUSEKEEPING

# temporary route for api testing
@app.post('/api/test')
async def test_query(query: UserQuery):
    log.debug("/api/test accessed", query, query.query)
    # print('user query: ', query.query)
    return { "type": "response", "body": query }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
