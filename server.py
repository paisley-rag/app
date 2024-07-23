from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import shutil
import os
import use_s3

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
    return {"message": "Server running"}


@app.get('/api/evals')
async def get_evals():
    eval_table = await evals.get_evals()
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

    return {"message": f"{file.filename} received"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
