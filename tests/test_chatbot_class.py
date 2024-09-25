'''
Tests for chatbot_class Chatbot
- Note: LlamaIndex not tested, does not include 'query' or 'prompt'
'''
import logging
import pytest
from db.tests.kb_test_constants import (
    client_sentence_config,
)
from db.tests.chatbot_test_configs import chatbot_config
from db.chatbot.chatbot_class import Chatbot

@pytest.fixture(scope="function")
def prep_kb(client, jwt_headers):
    # setup kb
    kb_post_response = client.post(
        '/api/knowledge-bases',
        json=client_sentence_config,
        headers=jwt_headers
    )
    assert kb_post_response.status_code == 200
    kb_id = kb_post_response.json()['id']

    with open('./db/tests/query_test_content.txt', 'rb') as f:
        kb_upload_response = client.post(
            f'/api/knowledge-bases/{id}/upload',
            files={'file': ("query_test_content.txt", f, "text/plain")},
            headers=jwt_headers
        )
    assert kb_upload_response.status_code == 200
    yield kb_id

    # clean up
    client.post(
        '/api/knowlege-bases/{kb_id}/delete',
        headers=jwt_headers
    )

@pytest.fixture(scope="function")
def mocked_fcts(mocker):
    mocker.patch(
        'db.chatbot.chatbot_class.SimilarityPostprocessor.postprocess_nodes',
        return_value='testing'
    )
    mocker.patch(
        'db.chatbot.chatbot_class.ColbertRerank.postprocess_nodes',
        return_value='testing'
    )
    mocker.patch(
        'db.chatbot.chatbot_class.LongContextReorder.postprocess_nodes',
        return_value='testing'
    )

@pytest.mark.asyncio
async def test_all_false(prep_kb, test_db, client, jwt_headers, mocked_fcts):
    kb_id = prep_kb

    # setup chatbot
    chatbot_post_response = client.post(
        '/api/chatbots',
        json=chatbot_config(kb_id)['base'],
        headers=jwt_headers
    )
    assert chatbot_post_response.status_code == 200
    chatbot_id = chatbot_post_response.json()['id']
    assert chatbot_id != ''

    # test
    get_response = client.get(f'/api/chatbots/{chatbot_id}', headers=jwt_headers)
    data_obj = get_response.json()
    logging.info(data_obj)
    assert data_obj['similarity']['on'] is False
    assert data_obj['colbert_rerank']['on'] is False
    assert data_obj['long_context_reorder']['on'] is False

    c = Chatbot(chatbot_id, test_db)

    assert not c._process_similarity([])
    assert not c._process_colbert([], 'query')
    assert not c._process_reorder([])

@pytest.mark.asyncio
async def test_similarity_only(prep_kb, test_db, client, jwt_headers, mocked_fcts):
    kb_id = prep_kb

    # setup chatbot
    chatbot_post_response = client.post(
        '/api/chatbots',
        json=chatbot_config(kb_id)['similarity_only'],
        headers=jwt_headers
    )
    assert chatbot_post_response.status_code == 200
    chatbot_id = chatbot_post_response.json()['id']
    assert chatbot_id != ''

    # test
    get_response = client.get(f'/api/chatbots/{chatbot_id}', headers=jwt_headers)
    data_obj = get_response.json()
    logging.info(data_obj)
    assert data_obj['similarity']['on'] is True
    assert data_obj['colbert_rerank']['on'] is False
    assert data_obj['long_context_reorder']['on'] is False

    c = Chatbot(chatbot_id, test_db)

    assert c._process_similarity([]) == 'testing'
    assert not c._process_colbert([], 'query')
    assert not c._process_reorder([])

@pytest.mark.asyncio
async def test_colbert_only(prep_kb, test_db, client, jwt_headers, mocked_fcts):
    kb_id = prep_kb

    # setup chatbot
    chatbot_post_response = client.post(
        '/api/chatbots',
        json=chatbot_config(kb_id)['colbert_only'],
        headers=jwt_headers
    )
    assert chatbot_post_response.status_code == 200
    chatbot_id = chatbot_post_response.json()['id']
    assert chatbot_id != ''

    # test
    get_response = client.get(f'/api/chatbots/{chatbot_id}', headers=jwt_headers)
    data_obj = get_response.json()
    logging.info(data_obj)
    assert data_obj['similarity']['on'] is False
    assert data_obj['colbert_rerank']['on'] is True
    assert data_obj['long_context_reorder']['on'] is False

    c = Chatbot(chatbot_id, test_db)

    assert not c._process_similarity([])
    assert c._process_colbert([], 'query') == 'testing'
    assert not c._process_reorder([])

@pytest.mark.asyncio
async def test_similarity_colbert(prep_kb, test_db, client, jwt_headers, mocked_fcts):
    kb_id = prep_kb

    # setup chatbot
    chatbot_post_response = client.post(
        '/api/chatbots',
        json=chatbot_config(kb_id)['similarity_colbert'],
        headers=jwt_headers
    )
    assert chatbot_post_response.status_code == 200
    chatbot_id = chatbot_post_response.json()['id']
    assert chatbot_id != ''

    # test
    get_response = client.get(f'/api/chatbots/{chatbot_id}', headers=jwt_headers)
    data_obj = get_response.json()
    logging.info(data_obj)
    assert data_obj['similarity']['on'] is True
    assert data_obj['colbert_rerank']['on'] is True
    assert data_obj['long_context_reorder']['on'] is False

    c = Chatbot(chatbot_id, test_db)

    assert c._process_similarity([]) == 'testing'
    assert c._process_colbert([], 'query') == 'testing'
    assert not c._process_reorder([])
