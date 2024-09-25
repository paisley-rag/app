'''
Tests for chatbot API routes
'''
import logging

import pytest

@pytest.mark.asyncio
async def test_get_all_chatbots_200(client, jwt_headers):
    response = client.get('/api/chatbots', headers=jwt_headers)
    assert response.status_code == 200
    # assert len(response.json()) == 0

@pytest.mark.asyncio
async def test_get_single_chatbot_not_found(client, jwt_headers):
    response = client.get('/api/chatbots/3', headers=jwt_headers)
    assert response.status_code == 200
    assert "no chatbot configuration found" in response.json().values()

@pytest.mark.asyncio
async def test_add_get_single_chatbot(client, jwt_headers):
    new_chatbot_data = {
        "name": "testchatbot",
        "knowledge_bases": [],
        "generative_model": "gpt-4-o",
        "similarity": {
            "on": False
            },
        "colbert_rerank": {
            "on": False
            },
        "long_context_reorder": {
            "on": False
            },
        "prompt": ""
    }
    post_response = client.post('/api/chatbots', json=new_chatbot_data, headers=jwt_headers)
    assert post_response.status_code == 200
    id = post_response.json()['id']

    get_response = client.get(f'/api/chatbots/{id}', headers=jwt_headers)
    data_obj = get_response.json()
    assert data_obj['generative_model'] == 'gpt-4-o'

@pytest.mark.asyncio
async def test_add_put_single_chatbot(client, jwt_headers):
    new_chatbot_data = {
        "name": "testchatbot",
        "knowledge_bases": [],
        "generative_model": "gpt-4-o",
        "similarity": {
            "on": False
            },
        "colbert_rerank": {
            "on": False
            },
        "long_context_reorder": {
            "on": False
            },
        "prompt": ""
    }
    post_response = client.post('/api/chatbots', json=new_chatbot_data, headers=jwt_headers)
    assert post_response.status_code == 200
    logging.info(f'******************* {post_response.json()}')
    id = post_response.json()['id']
    assert id

    updated_data = {
        "name": "testchatbot",
        "knowledge_bases": [],
        "generative_model": "gpt-4o-mini",
        "similarity": {
            "on": False
            },
        "colbert_rerank": {
            "on": False
            },
        "long_context_reorder": {
            "on": True
            },
        "prompt": ""
    }
    put_response = client.put(f'/api/chatbots/{id}/update', json=updated_data, headers=jwt_headers)
    assert put_response.status_code == 200

    get_response = client.get(f'/api/chatbots/{id}', headers=jwt_headers)
    data_obj = get_response.json()
    assert data_obj['generative_model'] == 'gpt-4o-mini'
    assert data_obj['long_context_reorder']['on'] == True

@pytest.mark.asyncio
async def test_add_delete_chatbot(client, jwt_headers):
    new_chatbot_data = {
        "name": "testchatbot",
        "knowledge_bases": [],
        "generative_model": "gpt-4-o",
        "similarity": {
            "on": False
            },
        "colbert_rerank": {
            "on": False
            },
        "long_context_reorder": {
            "on": False
            },
        "prompt": ""
    }
    post_response = client.post('/api/chatbots', json=new_chatbot_data, headers=jwt_headers)
    assert post_response.status_code == 200
    id = post_response.json()['id']

    get_response1 = client.get(f'/api/chatbots/{id}', headers=jwt_headers)
    logging.info('********* get-response1', get_response1.json())
    assert get_response1.json()['name'] == 'testchatbot'

    del_response = client.delete(f'/api/chatbots/{id}/delete', headers=jwt_headers)
    assert del_response.status_code == 200

    get_response2 = client.get(f'/api/chatbots/{id}', headers=jwt_headers)
    logging.info('********* get-response2', get_response2.json())
    assert get_response2.json()['message'] == 'no chatbot configuration found'

