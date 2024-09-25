'''
/api/knowledge-bases routes
'''
from fastapi import Request, APIRouter, File, UploadFile, Depends

import db.app_logger as log
from db.knowledge_base.kb_utils import create_kb_config
from db.db.session import get_db
from db.knowledge_base.kb_class import KnowledgeBase


router = APIRouter(
    prefix='/api/knowledge-bases',
)


# get all knowledge bases
@router.get("/")
async def get_knowledge_bases(kb_db=Depends(get_db)):
    result = kb_db.get_knowledge_bases()
    log.info('/api/knowledge-bases ', result)
    return result

# create a knowledge base
@router.post('/')
async def create_knowledge_base(request: Request, kb_db=Depends(get_db)):
    client_config = await request.json()

    if kb_db.knowledge_base_name_taken(client_config['kb_name']):
        message = f"{client_config['kb_name']} already exists"
        return {"message": message}

    kb_config = create_kb_config(client_config)
    result = kb_db.insert_knowledge_base(kb_config)
    kb_id = str(result.inserted_id)
    kb_db.add_id_to_kb_config(kb_config["kb_name"], kb_id)

    log.info("POST api/knowledge-bases : knowledge base created: ", result)
    new_kb = kb_db.get_knowledge_base(kb_id)

    return new_kb

# get one knowledge base's configuration details
@router.get("/{id}")
async def get_knowledge_base(id: str, kb_db=Depends(get_db)):
    kb_config = kb_db.get_knowledge_base(id)
    log.info('/api/knowledge-bases/', 'id', id, 'kb_config', kb_config)

    if kb_config:
        return kb_config

    return { "message": f"{id} does not exist" }

@router.delete("/{id}/delete")
async def delete_knowledge_base(id: str, kb_db=Depends(get_db)):
    result = kb_db.delete_knowledge_base(id)
    if result.deleted_count == 1:
        return {"message": f"{id} deleted"}

    return {"message": f"{id} does not exist"}

# add a file to a knowledge base
@router.post('/{id}/upload')
async def upload_file(id: str, file: UploadFile=File(...), kb_db=Depends(get_db)):
    log.info(f"/api/knowledge-bases/{id}/upload  file: {file.filename}")
    if not kb_db.get_knowledge_base(id):
        log.info(f'/api/knowledge-bases/{id}/upload', f"knowledge base {id} doesn't exist")
        return {"message": f"Knowledge base {id} doesn't exist"}

    if kb_db.file_exists(id, file):
        log.info(f'/api/knowledge-bases/{id}/upload', f"{file.filename} already in knowledge base")
        return {"message": f"{file.filename} already in knowledge base"}

    kb = KnowledgeBase(id, kb_db)
    log.info(f"/api/knowledge-bases/{id}/upload  uploading file: {file.filename}")

    try:
        await kb.ingest_file(file)
        log.info(f"/api/knowledge-bases/{id}/upload  {file.filename} uploaded")
        return {"message": f"{file.filename} uploaded"}
    except Exception as e:
        log.error(f"/api/knowledge-bases/{id}/upload  *****ERROR uploading {file.filename}")
        return {"message": f"Error: {e}"}
