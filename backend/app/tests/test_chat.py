from app.main import app
from fastapi.testclient import TestClient
from datetime import timezone, datetime
import pytest
import uuid

test_client = TestClient(app)

# Test data
TEST_USER = {
    "username": "srgtkrvvv",
    "password": "2-Bev45rt"
}

def get_auth_headers():
    """Helper function to get authentication headers"""
    # First ensure the test user exists
    test_client.post("/signup", json={
        "username": TEST_USER["username"],
        "password": TEST_USER["password"],
        "email": "test@example.com",
        "is_active": True,
        "is_superuser": False
    })
    
    login_response = test_client.post("/token", data=TEST_USER)
    token = login_response.json().get('access_token')
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
def test_conversation():
    """Create a test conversation and return its ID"""
    headers = get_auth_headers()
    response = test_client.post("/conversations/new-conversation", headers=headers)
    return response.json()

# Chat creation tests
def test_create_conversation():
    headers = get_auth_headers()
    response = test_client.post("/conversations/new-conversation", headers=headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New chat"
    assert "date_changed" in data
    assert "id" in data
    assert uuid.UUID(data["id"])  # Verify it's a valid UUID

def test_create_conversation_unauthorized():
    response = test_client.post("/conversations/new-conversation")
    assert response.status_code == 401

# Conversation retrieval tests
def test_get_user_conversations():
    headers = get_auth_headers()
    response = test_client.get("/conversations", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    for conv in response.json():
        assert "id" in conv
        assert "title" in conv
        assert "date_changed" in conv

def test_get_specific_conversation(test_conversation):
    headers = get_auth_headers()
    response = test_client.get(
        f"/conversations/{test_conversation['id']}", 
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert "conversation" in data
    assert "messages" in data
    assert data["conversation"]["id"] == test_conversation["id"]

def test_get_nonexistent_conversation():
    headers = get_auth_headers()
    fake_id = str(uuid.uuid4())
    response = test_client.get(f"/conversations/{fake_id}", headers=headers)
    assert response.status_code == 404

# Conversation update tests
def test_update_conversation(test_conversation):
    headers = get_auth_headers()
    new_title = "Updated Chat Title"
    response = test_client.put(
        f"/conversations/{test_conversation['id']}", 
        json={"title": new_title},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == new_title

def test_update_nonexistent_conversation():
    headers = get_auth_headers()
    fake_id = str(uuid.uuid4())
    response = test_client.put(
        f"/conversations/{fake_id}", 
        json={"title": "New Title"},
        headers=headers
    )
    assert response.status_code == 404

# Message tests
def test_send_message(test_conversation):
    headers = get_auth_headers()
    message_content = "Test message"
    response = test_client.post(
        f"/conversations/{test_conversation['id']}/send_message",
        params={"message_content": message_content},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == message_content
    assert "id" in data
    assert "date" in data

def test_send_message_to_nonexistent_conversation():
    headers = get_auth_headers()
    fake_id = str(uuid.uuid4())
    response = test_client.post(
        f"/conversations/{fake_id}/send_message",
        params={"message_content": "Test message"},
        headers=headers
    )
    assert response.status_code == 404

# Delete conversation tests
def test_delete_conversation(test_conversation):
    headers = get_auth_headers()
    response = test_client.delete(
        "/conversations/delete",
        json={"id": test_conversation["id"]},
        headers=headers
    )
    assert response.status_code == 201

    # Verify conversation is deleted
    get_response = test_client.get(
        f"/conversations/{test_conversation['id']}", 
        headers=headers
    )
    assert get_response.status_code == 404

def test_delete_nonexistent_conversation():
    headers = get_auth_headers()
    fake_id = str(uuid.uuid4())
    response = test_client.delete(
        "/conversations/delete",
        json={"id": fake_id},
        headers=headers
    )
    # Should still return 201 as per current implementation
    assert response.status_code == 201


