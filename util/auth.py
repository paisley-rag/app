'''
Utility function for API route authorization
- expected header key 'X-API-Key'
- will check mongo/docdb in configs/config_api collection for existence of the given key

- unused with current JWT auth scheme
'''

from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader


import db.util.mongo_api_util as mutil
import db.app_logger as log

api_key_header = APIKeyHeader(name="X-API-Key")

def check_key(api_key_header: str = Security(api_key_header)):
    log.info(f"util/auth.py check_key: X-API-Key {api_key_header}")
    if mutil.key_exists(api_key_header):
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )
