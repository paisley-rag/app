from fastapi import Request, APIRouter, Depends
from pydantic import BaseModel

import db.app_logger as log
from db.chatbot.chatbot_class import Chatbot
from db.db.session import get_db

router = APIRouter(
    prefix='/api/chatbots'
)

class UserQuery(BaseModel):
    query: str

class QueryBody(UserQuery):
    chatbot_id: str

@router.get('/')
async def get_chatbots(chatbot_db=Depends(get_db)):
    log.info('/api/chatbots loaded')
    results = chatbot_db.get_all_chatbots()
    return results

@router.get('/{id}')
async def get_chatbots_id(id: str, chatbot_db=Depends(get_db)):
    results = chatbot_db.get_one_chatbot(id)
    log.info(f"/api/chatbots/{id}: ", results)
    if not results:
        return {"message": "no chatbot configuration found"}

    return results

@router.post('/')
async def post_chatbots(request: Request, chatbot_db=Depends(get_db)):
    body = await request.json()
    log.info(f"/api/chatbots POST body: ", body)

    # add the default prompt to all created chatbots
    # - gives the user something to modify
    body['prompt'] = Chatbot.get_default_prompt()

    if chatbot_db.chatbot_name_taken(body["name"]):
        message = f"A chatbot named {body['name']} already exists"
        return {"message": message}
    else:
        result = chatbot_db.insert_chatbot(body)
        inserted_id = str(result.inserted_id)
        chatbot_db.add_id_to_chatbot_config(body["name"], inserted_id)

        new_chatbot = chatbot_db.get_one_chatbot(inserted_id)
        print("new_chatbot: ", new_chatbot)

        return new_chatbot

@router.put('/{id}/update')
async def update_chatbot(id: str, request: Request, chatbot_db=Depends(get_db)):
    body = await request.json()
    log.info(f"/api/chatbots/{id}/update body: ", body)

    result = chatbot_db.update_chatbot(id, body)
    return result

@router.delete('/{id}/delete')
async def delete_chatbot(id: str, chatbot_db=Depends(get_db)):
    log.info(f"/api/chatbots DELETE request received for {id}")
    result = chatbot_db.delete_chatbot(id)
    if result.deleted_count == 1:
        return {"message": f"{id} deleted"}
    else:
        return {"message": f"{id} does not exist"}
