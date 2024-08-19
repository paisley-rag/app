'''
Initial structure if routes specific to users / auth / API management are required
- currently, unused
'''
from fastapi import APIRouter

import db.app_logger as log
import db.util.mongo_api_util as mutil

router = APIRouter(
    prefix='/api/auth',
)

@router.get('/')
async def get_keys():
    log.info('/api/auth loaded')
    return { "keys": None }
