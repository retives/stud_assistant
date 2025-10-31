from app.main import app
from fastapi.testclient import TestClient

test_client = TestClient(app)

# Login test
def test_login():
    response = test_client.post("/token", data={"username": "srgtkrvvv", "password": "2-Bev45rt"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_nonexistent_user_login():
    response = test_client.post("/token", data={"username": "nonexistent", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username"}

def test_incorrect_password_login():
    respionse = test_client.post("/token", data={"username": "srgtkrvvv", "password": "wrongpassword"})
    assert respionse.status_code == 401
    assert respionse.json() == {"detail": "Incorrect password"}


# Signup tests
def test_correct_singup():
    response = test_client.post("/signup", json={
        'email': 'newtestuser@example.com',
        'username': 'new_test_user',
        'password': 'Pass_w143',
        'is_active': True,
        'is_superuser': False
        })
    assert response.status_code == 200
    assert "access_token" in response.json()
    
# Delete user
def test_delete_user():
    response = test_client.delete("/delete-account", data={
        'user_id': 'f223c6ca-4448-4316-8061-3666ecf36d31 | new_test_user | newtestuser@example.com | $argon2id$v=19$m=65536,t=3,p=4$Rqi1Nuac8957L8UYozSm1A$GQNcIZqDyZah44miE7cz1RHfXfwEL8ac2nPS40K2G1s'
        })
    assert response.status_code == 200
    get_response = test_client.get("/user/f223c6ca-4448-4316-8061-3666ecf36d31")
    assert get_response.status_code == 404
# User retreival tests


def test_current_user():
    login_response = test_client.post("/token", data={"username": "srgtkrvvv", "password": "2-Bev45rt"})
    token = login_response.json().get("access_token")
    print(token)
    response = test_client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json().get("username") == "srgtkrvvv"

def test_user_list():
    response = test_client.get("/list-users/")
    print(response)
    assert response.status_code == 200


