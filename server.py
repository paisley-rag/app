import os
import json
from datetime import timedelta

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm

import nest_asyncio

import db.app_logger as log
import db.evals.evals as evals
import db.evals.eval_utils as eval_utils
import db.pipeline.query as pq
import db.util.jwt as jwt

from db.celery.tasks import run_evals_background
from db.routers import chatbots
from db.routers import api_auth
from db.routers import knowledge_bases

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# test if we need this w/n the server
nest_asyncio.apply()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# app.include_router(
#    api_auth.router,
#    dependencies=[Depends(jwt.get_current_user)]
#)

app.include_router(
    chatbots.router,
    dependencies=[Depends(jwt.get_current_user)]
)

app.include_router(
    knowledge_bases.router,
    dependencies=[Depends(jwt.get_current_user)]
)

@app.post("/api/token", response_model=jwt.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = jwt.authenticate_user(jwt.user_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}




@app.get('/api')
async def root():
    log.info("server running")
    return {"message": "Server running"}


# query route
@app.post('/api/query')
async def post_query(body: pq.QueryBody, auth: bool = Depends(jwt.get_current_user)):
    response = pq.post_query(body)
    if response:
      context, output = eval_utils.extract_from_response(response)
      log.info(f"Adding background task for chatbot_id: {body.chatbot_id}, query: {body.query}, output: {output}")
      run_evals_background.delay(
          body.chatbot_id,
          body.query,
          context,
          output
      )
    return response

@app.get('/api/history')
async def get_evals(auth: bool = Depends(jwt.get_current_user)):
    data = evals.get_chat_history()
    return data

@app.get('/api/scores')
async def get_scores(auth: bool = Depends(jwt.get_current_user)):
    config_path = os.path.join(os.path.dirname(__file__), 'evals', 'eval_config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)
    scores = config.get('scores', [])
    return scores


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
