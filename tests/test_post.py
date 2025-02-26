import pytest
from user.models import User
from post.models import Post

@pytest.mark.django_db
def test_create_post(api_client):
    user = User.objects.create_superuser(email="test@example.com", password="Test1234", name="testuser")
    api_client.force_authenticate(user=user) 
    response = api_client.post("/post/", {"title": "Hello, world!", "post":"Hello world!, hello work and bla bla", 'sentiment':'positive'})
    
    assert response.status_code == 201
    assert response.data["title"] == "Hello, world!"

@pytest.mark.django_db
def test_get_posts(api_client):
    response = api_client.get("/post/list/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_detail_get(api_client):
    post = Post.objects.create(title = "Hello, world!", post = "Hello world!, hello work and bla bla", sentiment = 'positive')

    detail_post =  api_client.get(f'/post/{post.id}/')

    assert detail_post.status_code == 200