'''
Tests auth for server routes
- JWT vs non-JWT
'''
import pytest

# test unprotected route
@pytest.mark.asyncio
async def test_api_returns_200(client):
    response = client.get("/api")
    assert response.status_code == 200

# test route with no jwt header
@pytest.mark.asyncio
async def test_kb_returns_401(client):
    response = client.get("/api/knowledge-bases")
    assert response.status_code == 401

# test route WITH jwt header
@pytest.mark.asyncio
async def test_kb_returns_200(client, jwt_headers):
    response = client.get("/api/knowledge-bases", headers=jwt_headers)
    assert response.status_code == 200

# test route with no jwt header
@pytest.mark.asyncio
async def test_chatbots_returns_401(client):
    response = client.get("/api/chatbots")
    assert response.status_code == 401

# test route WITH jwt header
@pytest.mark.asyncio
async def test_chatbots_returns_200(client, jwt_headers):
    response = client.get("/api/chatbots", headers=jwt_headers)
    assert response.status_code == 200
