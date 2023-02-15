from django.test import TestCase, Client
from django.shortcuts import reverse
import pytest
from User_manager.models import User, League
from django.contrib.auth.models import Group, Permission
# Create your tests here.
@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user_in_admin_group():
    user = User.objects.create_user(
        first_name="first_name",
        last_name="last_name",
        username="test@test.pl",
        password='password', )
    group = Group.objects.create(name="admin")
    group.user_set.add(user)
    perms = Permission.objects.all()
    for item in perms:
        item.group_set.add(group)

@pytest.mark.django_db
def test_MainPage(client, user_in_admin_group):
    url = reverse('main_page')
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    assert response.status_code == 302
    assert response.url == '/'
    assert client.session.get('_auth_user_id') is not None



@pytest.mark.django_db
def test_login_view(client, user_in_admin_group):
    url = reverse('login')
    response = client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    assert response.status_code == 302
    assert response.url == '/'
    assert client.session.get('_auth_user_id') is not None
