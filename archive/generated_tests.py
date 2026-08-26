import requests
import pytest
import urllib3

# 1. Отключаем назойливые предупреждения о небезопасных запросах
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = "https://jsonplaceholder.typicode.com"

@pytest.fixture
def session():
    """Создаёт переиспользуемую сессию для HTTP-запросов."""
    s = requests.Session()
    
    # 2. ГЛАВНОЕ ИЗМЕНЕНИЕ: Отключаем проверку SSL-сертификатов для всей сессии
    s.verify = False 
    
    yield s
    s.close()

@pytest.fixture
def session():
       """Create a reusable session for making requests."""
       s = requests.Session()
       yield s
       s.close()

def test_get_posts(session):
       """Test the GET /posts endpoint."""
       response = session.get(f"{BASE_URL}/posts")
       assert response.status_code == 200
       assert isinstance(response.json(), list)

def test_get_post_by_id(session):
       """Test the GET /posts/:id endpoint."""
       post_id = 1
       response = session.get(f"{BASE_URL}/posts/{post_id}")
       assert response.status_code == 200
       data = response.json()
       assert isinstance(data, dict)
       assert data["id"] == post_id

def test_create_post(session):
       """Test the POST /posts endpoint."""
       new_post = {
           "title": "foo",
           "body": "bar",
           "userId": 1
       }
       response = session.post(f"{BASE_URL}/posts", json=new_post)
       assert response.status_code == 201
       created_post = response.json()
       assert created_post["title"] == new_post["title"]
       assert created_post["body"] == new_post["body"]
       assert created_post["userId"] == new_post["userId"]

def test_update_post(session):
       """Test the PUT /posts/:id endpoint."""
       post_id = 1
       updated_data = {
           "title": "foo",
           "body": "bar",
           "userId": 2
       }
       response = session.put(f"{BASE_URL}/posts/{post_id}", json=updated_data)
       assert response.status_code == 200
       updated_post = response.json()
       assert updated_post["id"] == post_id
       assert updated_post["title"] == updated_data["title"]
       assert updated_post["body"] == updated_data["body"]
       assert updated_post["userId"] == updated_data["userId"]

def test_delete_post(session):
       """Test the DELETE /posts/:id endpoint."""
       post_id = 100  # Assuming there's a post with id 100
       response = session.delete(f"{BASE_URL}/posts/{post_id}")
       assert response.status_code == 200