from app.main import app
from fastapi.testclient import TestClient

test_client = TestClient(app)

def test_login():
    response = test_client.post("/token", data={"username": "retives", "password": "2-Bev45rt"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_nonexistent_user_login():
    response = test_client.post("/token", data={"username": "nonexistent", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username"}

def test_incorrect_password_login():
    respionse = test_client.post("/token", data={"username": "retives", "password": "wrongpassword"})
    assert respionse.status_code == 401
    assert respionse.json() == {"detail": "Incorrect password"}
def test_user_list():
    response = test_client.get("/list-users/")
    print(response)
    assert response.status_code == 200

def test_current_user():
    login_response = test_client.post("/token", data={"username": "retives", "password": "2-Bev45rt"})
    token = login_response.json().get("access_token")
    print(token)
    response = test_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json().get("username") == "retives"




