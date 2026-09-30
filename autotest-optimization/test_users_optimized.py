import pytest
import requests

BASE_URL = "http://localhost:8000"

@pytest.fixture(params=[
    {"name": "Alice", "email": "alice@example.com", "expected_status": 201, "expected_name": "Alice"},
    {"name": "Bob", "email": "bob@example.com", "expected_status": 201, "expected_name": "Bob"},
    {"name": "Charlie", "email": "charlie@example.com", "expected_status": 201, "expected_name": "Charlie"},
    {"name": "Test", "email": "bad-email", "expected_status": 400, "expected_message": "Invalid email format"},
    {"name": "Test", "email": "test@example.com", "expected_status": 400, "expected_message": "Name is required"}
])
def user_data(request):
    return request.param

def test_create_user(user_data):
    payload = user_data
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == user_data["expected_status"]
    if "expected_name" in user_data:
        assert response.json()["name"] == user_data["expected_name"]
    if "expected_message" in user_data:
        assert response.json()["detail"] == user_data["expected_message"]