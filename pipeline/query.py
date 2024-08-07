import os

from pydantic import BaseModel

import db.app_logger as log
from db.pipeline.pipeline_class import Pipeline
# import pipeline.mongo_util as mutil
# import pipeline.config_util as cutil


class UserQuery(BaseModel):
    query: str

class QueryBody(UserQuery):
    chatbot_id: str

def post_query(body: QueryBody):
    log.info('/api/query body received: ',
             'body.query:', body.query,
             " body.chatbot_id:", body.chatbot_id
             )
    pipe = Pipeline(body.chatbot_id)
    log.info('/api/query pipeline retrieved')
    response = pipe.query(body.query)
    log.info('/api/query response:', response)
<<<<<<< HEAD
    return response
=======
    return { "type": "response", "body": response }
>>>>>>> main
