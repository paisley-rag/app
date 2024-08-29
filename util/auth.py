'''
Utility function for API route authorization
- expected header key 'X-API-Key'
- will check mongo/docdb in configs/config_api collection for existence of the given key
'''
import secrets
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

# from fastapi.security import APIKeyHeader


import db.util.mongo_api_util as mutil
import db.app_logger as log

security = HTTPBasic()

# api_key_header = APIKeyHeader(name="X-API-Key")

# def check_key(api_key_header: str = Security(api_key_header)):
#     log.info(f"util/auth.py check_key: X-API-Key {api_key_header}")
#     if mutil.key_exists(api_key_header):
#         return True
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Missing or invalid API key"
#     )

def check_key(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = b"admin"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = b"topsecret"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"www-authenticate": "Basic"},
        )
    return credentials.username