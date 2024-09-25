'''
Common pytest configurations for testing routes
'''
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from db.backend.app import app as paisley_app
from db.tests.utils import get_jwt_headers
from db.db.mongo import Mongo
from db.db.session import get_db
from db.config import settings


def _get_test_db():
    try:
        db = Mongo(settings.MONGO_URI)
        db.set_chatbot_db('testonly', settings.CONFIG_PIPELINE_COL)
        db.set_kb_db('testonly', settings.CONFIG_KB_COL)
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def app():
    print('pytest fixture app')
    yield paisley_app

@pytest.fixture(scope="function")
def client(app: FastAPI):
    app.dependency_overrides[get_db] = _get_test_db

    with TestClient(app) as client:
        yield client

    db = Mongo(settings.MONGO_URI)
    db.drop_db('testonly')
    db.close()

@pytest.fixture(scope="function")
def jwt_headers():
    return get_jwt_headers()

@pytest.fixture(scope="function")
def test_db():
    try:
        test_db = Mongo(settings.MONGO_URI)
        test_db.set_chatbot_db('testonly', settings.CONFIG_PIPELINE_COL)
        test_db.set_kb_db('testonly', settings.CONFIG_KB_COL)
        yield test_db
    finally:
        test_db.close()