'''
Tests for API knowledge-bases routes
'''
import os
import logging

import pytest

from db.tests.kb_test_constants import client_sentence_config

@pytest.mark.asyncio
async def test_get_all_kbs_200(client, jwt_headers):
    response = client.get('/api/knowledge-bases', headers=jwt_headers)
    assert response.status_code == 200
    assert len(response.json()) == 0

@pytest.mark.asyncio
async def test_add_get_single_kb(client, jwt_headers):
    post_response = client.post(
        '/api/knowledge-bases',
        json=client_sentence_config,
        headers=jwt_headers
    )
    assert post_response.status_code == 200
    id = post_response.json()['id']

    get_response = client.get(f'/api/knowledge-bases/{id}', headers=jwt_headers)
    data_obj = get_response.json()
    assert data_obj['kb_name'] == 'Sentence'
    assert data_obj['splitter'] == 'Sentence'
    assert data_obj['embed_config']['embed_model'] == 'text-embedding-3-small'

@pytest.mark.asyncio
async def test_add_delete_single_kb(client, jwt_headers):
    post_response = client.post(
        '/api/knowledge-bases',
        json=client_sentence_config,
        headers=jwt_headers
    )
    assert post_response.status_code == 200
    id = post_response.json()['id']

    get_response = client.get(f'/api/knowledge-bases/{id}', headers=jwt_headers)
    data_obj = get_response.json()
    assert data_obj['kb_name'] == 'Sentence'
    assert data_obj['splitter'] == 'Sentence'
    assert data_obj['embed_config']['embed_model'] == 'text-embedding-3-small'

    client.delete(f'/api/knowledge-bases/{id}/delete', headers=jwt_headers)
    get_response2 = client.get(f'/api/knowledge-bases/{id}', headers=jwt_headers)
    assert f"{id} does not exist" in get_response2.json()['message']


@pytest.mark.asyncio
async def test_upload_single_kb(client, jwt_headers):
    post_response = client.post(
        '/api/knowledge-bases',
        json=client_sentence_config,
        headers=jwt_headers
    )
    id = post_response.json()['id']

    # upload file
    testfile = open('./db/tests/testfile.txt', 'a', encoding="utf-8")
    testfile.write('test content')

    with open('./db/tests/testfile.txt', 'rb') as f:
        upload_response = client.post(
            f'/api/knowledge-bases/{id}/upload',
            files={'file': ("testfile.txt", f, "text/plain")},
            headers=jwt_headers
        )

    logging.info('******* upload_response')
    logging.info(upload_response)
    data_obj = upload_response.json()
    assert upload_response.status_code == 200
    assert 'testfile.txt uploaded' in data_obj['message']
    assert os.path.isfile('./tmpfiles/testfile.txt')

    client.delete(f'/api/knowledge-bases/{id}/delete', headers=jwt_headers)
    get_response2 = client.get(f'/api/knowledge-bases/{id}', headers=jwt_headers)
    assert f"{id} does not exist" in get_response2.json()['message']

    os.remove('./db/tests/testfile.txt')
    os.remove('./tmpfiles/testfile.txt')
