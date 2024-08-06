
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
import nest_asyncio
from dotenv import load_dotenv

# import app_logger as log
# import use_s3
import db.knowledge_base.routes as kb

nest_asyncio.apply()

# env = os.getenv("ENV")
# print(env)
# if env == 'testing':
#     load_dotenv(override=True, dotenv_path='.env.testing')
# else:
#     load_dotenv(override=True)

# MONGO_URI = os.environ["MONGO_URI"]
# CONFIG_DB = os.environ["CONFIG_DB"]
# # print(CONFIG_DB)
# CONFIG_PIPELINE_COL = os.environ["CONFIG_PIPELINE_COL"]

print("Starting server")
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
    # log.info("server running")
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

        

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')