import pytest
from rest_framework.test import APIClient
from user.models import User


@pytest.mark.django_db
def test_get_user_list(api_client):
    user = api_client.post("/user/users/", {'email':'test@gmail.com', 'password': 'test2025', 'name': 'test'}, format="json")
    response = api_client.get("/user/users/")
    assert response.status_code == 200
    assert len(response.data) > 0
    assert user.status_code == 201

@pytest.mark.django_db
def test_create_user(api_client):
    user = api_client.post("/user/users/", {'email':'test@gmail.com', 'password': 'test2025', 'name': 'test'})
    assert user.status_code == 201

@pytest.mark.django_db
def test_detail_getuser(api_client):
    user = User.objects.create_user(email='test@gmail.com', password='test2025', name='test')
    api_client.force_authenticate(user=user) 
    response = api_client.get(f'/user/{user.id}/')

    assert response.status_code == 200