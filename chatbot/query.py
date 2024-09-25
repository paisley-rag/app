'''
class and functions specific to the /api/query route
- imported in server.py
'''
from pydantic import BaseModel

import db.app_logger as log
from db.chatbot.chatbot_class import Chatbot


class UserQuery(BaseModel):
    query: str

class QueryBody(UserQuery):
    chatbot_id: str

def post_query(body: QueryBody, db):
    log.info('chatbot/query.py    /api/query body received: ',
             'body.query:', body.query,
             " body.chatbot_id:", body.chatbot_id
             )
    pipe = Chatbot(body.chatbot_id, db)
    log.info('chatbot/query.py    /api/query chatbot retrieved')
    response = pipe.query(body.query)
    log.info('chatbot/query.py    /api/query response:', response)
    return response
