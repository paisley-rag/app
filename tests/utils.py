'''
utilities for testing
'''
from db.util import jwt
from db.config import settings

def get_jwt_headers():
    token = jwt.create_access_token({
        "sub": settings.PAISLEY_ADMIN_USERNAME
    })
    return { "Authorization" : f"Bearer {token}" }
