'''
"Wrapper" server.py file
- created to minimize overall structural changes to project
- facilitates more traditional pytest structure for testing
'''
import os

import uvicorn
import nest_asyncio
from dotenv import load_dotenv
from db.backend.app import app

load_dotenv(override=True)

if __name__ == '__main__':
    nest_asyncio.apply()
    if os.environ['ENVIRONMENT'] != 'production':
        print('non-production environment')
        uvicorn.run("db.backend.app:app", host="0.0.0.0", port=8000, loop='asyncio', reload=True)

    uvicorn.run(app, host="0.0.0.0", port=8000, loop='asyncio')
