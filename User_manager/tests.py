from django.test import TestCase, Client
from User_manager.models import User
from django.shortcuts import reverse, redirect
import pytest
# Create your tests here.
@pytest.fixture
def client():
    return Client()

@pytest.mark.django_db
def test_login_view(client):
    User.objects.create_user(
        first_name="first_name",
        last_name="last_name",
        username="test@test.pl",
        password='password',)
    url = reverse('login')
    response = client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    assert response.status_code == 302
    assert response.url == '/'
    assert client.session.get('_auth_user_id') is not None
