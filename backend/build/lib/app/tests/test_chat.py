from app.main import app
from fastapi.testclient import TestClient
from datetime import  timezone, datetime
from app.security import read_access_token
test_client = TestClient(app)

# Chat creation test
def test_create_conversation():
    login_response = test_client.post("/token", data={"username": "srgtkrvvv", "password": "2-Bev45rt"})
    response = test_client.post("/new-conversation", json={
        'owner_id': '97dee78c-37d7-450a-aff1-a765b0142d85'
    }, headers={"Authorization": f"Bearer {login_response.json().get('access_token')}"})
    assert response.status_code == 200
    assert response.json().get("title") == "New chat"
    assert response.json().get('date_changed') == datetime.now(timezone.utc).isoformat(timespec='seconds')

def test_create_conversation_with_wrong_owner():
    login_response = test_client.post("/token", data={"username": "srgtkrvvv", "password": "2-Bev45rt"})
    
    # Use a different valid UUID that doesn't match the logged-in user's ID
    response = test_client.post("/new-conversation", json={
        'owner_id': 'a7dee78c-37d7-450a-aff1-a765b0142d85'  # Different valid UUID
    }, headers={"Authorization": f"Bearer {login_response.json().get('access_token')}"})
    assert response.status_code == 403
    assert response.json() == {"detail": "You can only create conversations for yourself."}

def test_get_user_conversations():
    login_response = test_client.post("/token", data={"username": "srgtkrvvv", "password": "2-Bev45rt"})
    response = test_client.get("/conversations", headers={"Authorization": f"Bearer {login_response.json().get('access_token')}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_delete_conversation():
    login_repsonse = test_client.post('/token', data={"username": "srgtkrvvv", "password": "2-Bev45rt"})
    owner_id = login_repsonse.json().get('access_token')
    response = test_client.delete('/delete', json={
        'owner_id': ,
        'id': 'c1dee78c-37d7-450a-aff1-a765b0142d85'
    }, headers={"Authorization": f"Bearer {
