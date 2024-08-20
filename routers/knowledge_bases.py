from fastapi import Request, APIRouter, File, UploadFile

import db.app_logger as log
import db.knowledge_base.routes as kb


router = APIRouter(
    prefix='/api/knowledge-bases',
)


# get all knowledge bases
@router.get("/")
async def get_knowledge_bases():
    return kb.get_all()

# create a knowledge base
@router.post('/')
async def create_knowledge_base(request: Request):
    client_config = await request.json()
    return kb.create(client_config)

# get one knowledge base's configuration details
@router.get("/{id}")
async def get_knowledge_base(id: str):
    return kb.get_one(id)

@router.delete("/{id}/delete")
async def delete_knowledge_base(id: str):
    return kb.delete(id)

# add a file to a knowledge base
@router.post('/{id}/upload')
async def upload_file(id: str, file: UploadFile=File(...)):
    try:
        return await kb.upload_file(id, file)
        
    except Exception as e:
        return {"message": f"Error: {e}"}