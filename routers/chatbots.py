from fastapi import Request, APIRouter
from pydantic import BaseModel

import db.app_logger as log
import db.pipeline.mongo_util as mutil
import db.knowledge_base.routes as convert

router = APIRouter(
    prefix='/api/chatbots'
)

class UserQuery(BaseModel):
    query: str

class QueryBody(UserQuery):
    chatbot_id: str

@router.get('/')
async def get_chatbots():
    log.info('/api/chatbots loaded')
    results = mutil.get_all_pipelines()
    log.info('/api/chatbots results:', results)
    return results

@router.get('/{id}')
async def get_chatbots_id(id: str):
    results = mutil.get_one_pipeline(id)
    log.info(f"/api/chatbots/{id}: ", results)
    if not results:
        return {"message": "no chatbot configuration found"}

    return results

@router.post('/')
async def post_chatbots(request: Request):
    body = await request.json()
    log.info(f"/api/chatbots POST body: ", body)
    
    if mutil.pipeline_name_taken(body["name"]):
        message = f"A pipeline named {body['name']} already exists"
        return {"message": message}
    
    else:

        # ugly but effective
        # can refactor later
        # postprocessing = body.get("postprocessing")
        # result = {}
        # for key in postprocessing:
        #     result[key] = convert.str_to_nums(postprocessing[key])
        # body["postprocessing"] = result

        # print("body: ", body)
        # input("press enter to continue")

        result = mutil.insert_pipeline(body)
        inserted_id = str(result.inserted_id)
        mutil.add_id_to_pipeline_config(body["name"], inserted_id)

        new_pipeline = mutil.get_one_pipeline(inserted_id)
        print("new_pipeline: ", new_pipeline)

        return new_pipeline

@router.put('/{id}/update')
async def update_chatbot(id: str, request: Request):
    body = await request.json()
    log.info(f"/api/chatbots/{id}/update body: ", body)

    result = mutil.update_pipeline(id, body)
    return result

@router.delete('/{id}/delete')
async def delete_chatbot(id: str):
    log.info(f"/api/chatbots DELETE request received for {id}")
    result = mutil.delete_pipeline(id)
    if result.deleted_count == 1:
        return {"message": f"{id} deleted"}
    else:
        return {"message": f"{id} does not exist"}
