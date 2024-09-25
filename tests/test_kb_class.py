'''
Tests for kb_class KnowledgeBase
- tests 'ingestion' methods within KnowledgeBase
- Note: saving file is tested in `test_kb_routes.py`
'''
import logging
import pytest
from fastapi import UploadFile
from db.tests.kb_test_constants import (
    client_sentence_config,
)
from db.knowledge_base.kb_class import KnowledgeBase

@pytest.mark.asyncio
async def test_kb_sentence_nodes_indexes(client, test_db, jwt_headers):
    # setup kb
    post_response = client.post('/api/knowledge-bases', json=client_sentence_config, headers=jwt_headers)
    id = post_response.json()['id']
    kb = KnowledgeBase(id, test_db)
    logging.info(kb._config)

    # Create text chunks
    nodes = await kb._create_nodes('./db/tests/query_test_content.txt')
    logging.info(f"********* {nodes}")
    assert type(nodes[0]).__name__ == 'TextNode'

    # Store indexes
    kb._store_indexes(nodes)
    vector_retriever = test_db.get_vector_retriever(id, 1)
    keyword_retriever = test_db.get_keyword_retriever(id, 1)
    logging.info(f"************* {vector_retriever}  {keyword_retriever}")
    assert type(vector_retriever).__name__ == 'VectorIndexRetriever'
    assert type(keyword_retriever).__name__ == 'BM25Retriever'


    # Add file to kb_config
    # - setup file
    with open('./db/tests/query_test_content.txt', 'rb') as testfile:
        file = UploadFile(testfile, filename='query_test_content.txt', headers={"content-type": "text/plain"})

    # - check before
    logging.info(kb._config)
    assert len(kb._config['files']) == 0

    kb._add_file_to_kb_config(file)

    # - check after
    logging.info(kb._config)
    assert len(kb._config['files']) == 1
