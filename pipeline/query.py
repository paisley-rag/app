'''
class and functions specific to the /api/query route
- imported in server.py
'''
from pydantic import BaseModel

import db.app_logger as log
from db.pipeline.pipeline_class import Pipeline


class UserQuery(BaseModel):
    query: str

class QueryBody(UserQuery):
    chatbot_id: str

def post_query(body: QueryBody):
    log.info('pipeline/query.py    /api/query body received: ',
             'body.query:', body.query,
             " body.chatbot_id:", body.chatbot_id
             )
    pipe = Pipeline(body.chatbot_id)
    log.info('pipeline/query.py    /api/query pipeline retrieved')
    response = pipe.query(body.query)
    log.info('pipeline/query.py    /api/query response:', response)
    return response
