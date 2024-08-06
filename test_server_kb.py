import os

import pymongo
from dotenv import load_dotenv
from fastapi.testclient import TestClient

from server_kb import app
from kb_test_constants import (
    client_sentence_config,
    client_semantic_config,
    client_llama_parse_config,
    server_sentence_config,
    server_semantic_config,
    server_llama_parse_config,
)

load_dotenv(override=True, dotenv_path=".env.testing")

MONGO_URI = os.environ["MONGO_URI"]
CONFIG_DB = os.environ["CONFIG_DB"]

client = TestClient(app)



def test_read_knowledge_bases():

    response = client.get("/api/knowledge-bases")
    assert response.status_code == 200
    assert response.json() == []

def test_create_simple_splitter_kb():
    response = client.post(
        "/api/knowledge-bases",
        json=client_sentence_config
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Sentence created"}

    response = client.post(
        "/api/knowledge-bases",
        json=client_sentence_config
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Sentence already exists"}

def test_create_semantic_splitter_kb():
    response = client.post(
        "/api/knowledge-bases",
        json=client_semantic_config
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Semantic created"}

    response = client.post(
        "/api/knowledge-bases",
        json=client_semantic_config
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Semantic already exists"}

def test_create_markdown_splitter_kb():
    response = client.post(
        "/api/knowledge-bases",
        json=client_llama_parse_config
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Markdown created"}

    response = client.post(
        "/api/knowledge-bases",
        json=client_llama_parse_config
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Markdown already exists"}

def test_get_kb_config():
    response = client.get("/api/knowledge-base/Sentence")
    assert response.status_code == 200
    assert response.json() == server_sentence_config

    response = client.get("/api/knowledge-base/unknown_kb")
    assert response.status_code == 200
    assert response.json() == {"message": "unknown_kb does not exist"}

# def test_upload_file():
#     response = client.post("/api/knowledge-bases/Sentence%20Splitter/upload", files={"file": ("test.txt", b"test")})
#     assert response.status_code == 200
#     assert response.json() == {"message": "test.txt uploaded"}

    # response = client.get("/api/knowledge-base/test_kb")
    # assert response.status_code == 200
    # assert response.json()["files"].length == 1

    # response = client.post("/api/knowledge-bases/unknown_kb/upload", files={"file": ("test.txt", b"test")})
    # assert response.status_code == 200
    # assert response.json() == {"message": "Knowledge base unknown_kb doesn't exist"}



