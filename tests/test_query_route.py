'''
Test query route
'''
import logging
import pytest
from db.tests.kb_test_constants import (
    client_sentence_config,
)
from db.tests.chatbot_test_configs import chatbot_config
from db.chatbot.chatbot_class import Chatbot

@pytest.mark.asyncio
async def test_query(client, jwt_headers):
    # setup kb
    kb_post_response = client.post('/api/knowledge-bases', json=client_sentence_config, headers=jwt_headers)
    assert kb_post_response.status_code == 200
    logging.info(f'*********** kb_post_response: {kb_post_response.json()}')
    kb_id = kb_post_response.json()['id']
    assert kb_id

    with open('./db/tests/query_test_content.txt', 'rb') as f:
        kb_upload_response = client.post(
            f'/api/knowledge-bases/{kb_id}/upload',
            files={'file': ("query_test_content.txt", f, "text/plain")},
            headers=jwt_headers
        )
    assert kb_upload_response.status_code == 200
    logging.info(f'**************** kb_upload_response:  {kb_upload_response.json()}')

    # setup chatbot
    chatbot_post_response = client.post('/api/chatbots', json=chatbot_config(kb_id)['base'], headers=jwt_headers)
    assert chatbot_post_response.status_code == 200
    # chatbot_id = chatbot_post_response.json()['id']

    chatbot_get_response = client.get('/api/chatbots', headers=jwt_headers)
    logging.info(f'*********** get_response {chatbot_get_response.json()}')
    chatbot_id = chatbot_get_response.json()[0]['id']
    assert chatbot_id

    # test
    query_body = {
        "chatbot_id": chatbot_id,
        "query": "tell me about Australia"
    }
    query_response = client.post(f'/api/query', json=query_body, headers=jwt_headers)
    logging.info(query_response.json()['response'])
    assert bool(query_response.json()['response']) == True

    # clean up
    client.delete(f'/api/knowledge-bases/{kb_id}/delete', headers=jwt_headers)
