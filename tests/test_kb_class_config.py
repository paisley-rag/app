'''
Tests for kb_class KnowledgeBase
- tests KnowledgeBase configuration from config json
'''
import logging
import pytest
from db.tests.kb_test_constants import (
    client_sentence_config,
    client_semantic_config,
    client_llama_parse_config,
)
from db.knowledge_base.kb_class import KnowledgeBase

@pytest.mark.asyncio
async def test_kb_sentence_config(client, test_db, jwt_headers):
    post_response = client.post(
        '/api/knowledge-bases',
        json=client_sentence_config,
        headers=jwt_headers
    )
    id = post_response.json()['id']
    kb = KnowledgeBase(id, test_db)
    logging.info(kb._config)

    assert kb._config['kb_name'] == client_sentence_config['kb_name']
    assert kb._config['ingest_method'] == client_sentence_config['ingest_method']
    assert kb._config['splitter'] == client_sentence_config['splitter']
    assert kb._config['embed_config'] == client_sentence_config['embed_config']
    assert kb._config['id'] == id
    assert "files" in kb._config

@pytest.mark.asyncio
async def test_kb_semantic_config(client, test_db, jwt_headers):
    post_response = client.post(
        '/api/knowledge-bases',
        json=client_semantic_config,
        headers=jwt_headers
    )
    id = post_response.json()['id']
    kb = KnowledgeBase(id, test_db)
    logging.info(kb._config)

    assert kb._config['kb_name'] == client_semantic_config['kb_name']
    assert kb._config['ingest_method'] == client_semantic_config['ingest_method']
    assert kb._config['splitter'] == client_semantic_config['splitter']
    assert kb._config['embed_config'] == client_semantic_config['embed_config']
    assert "embed_model" in kb._config['splitter_config']
    assert kb._config['id'] == id
    assert "files" in kb._config

@pytest.mark.asyncio
async def test_kb_llamaparse_config(client, test_db, jwt_headers):
    post_response = client.post(
        '/api/knowledge-bases',
        json=client_llama_parse_config,
        headers=jwt_headers
    )
    id = post_response.json()['id']
    kb = KnowledgeBase(id, test_db)
    logging.info(kb._config)

    assert kb._config['kb_name'] == client_llama_parse_config['kb_name']
    assert kb._config['ingest_method'] == client_llama_parse_config['ingest_method']
    assert kb._config['splitter'] == client_llama_parse_config['splitter']
    assert kb._config['embed_config'] == client_llama_parse_config['embed_config']
    assert "llm" in kb._config['splitter_config']
    assert kb._config['llm_config']['llm_provider'] == client_llama_parse_config['llm_config']['llm_provider']
    assert kb._config['llm_config']['llm_model'] == client_llama_parse_config['llm_config']['llm_model']
    assert kb._config['id'] == id
    assert "files" in kb._config
