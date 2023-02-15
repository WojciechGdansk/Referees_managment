from django.test import TestCase, Client
from django.shortcuts import reverse
import pytest
from User_manager.models import User, League
from django.contrib.auth.models import Group, Permission
from django.contrib.messages import get_messages


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
def test_SignUp(client):
    url = reverse('sign_up')
    users = User.objects.count()
    league = League.objects.create(which_league="testowa liga")
    response = client.post(url, {'first_name': 'first test',
                                 'last_name': 'last test',
                                 'phone_number': 1245789,
                                 'username': 'test@test.pl',
                                 'password': 'password',
                                 'password2': 'password',
                                 'league2': league.slug})
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Pomyślnie utworzono konto"
    assert User.objects.count() == users + 1


@pytest.mark.django_db
def test_login_view(client, user_in_admin_group):
    url = reverse('login')
    response = client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    assert response.status_code == 302
    assert response.url == '/'
    assert client.session.get('_auth_user_id') is not None


@pytest.mark.django_db
def test_logoutview(client, user_in_admin_group):
    user = User.objects.first()
    client.force_login(user)
    assert client.session.get('_auth_user_id') is not None
    url = reverse('logout')
    response = client.get(url)
    assert client.session.get('_auth_user_id') is None
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Wylogowano"


@pytest.mark.django_db
def test_ManageUsers(client, user_in_admin_group):
    url = reverse('manage_users')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
    user = User.objects.first()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_ManageGropus(client, user_in_admin_group):
    url = reverse('manage_groups')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
    user = User.objects.first()
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_GroupDetails(client, user_in_admin_group):
    user = User.objects.first()
    group = Group.objects.last()
    url = reverse("group_details", kwargs={"id": group.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_NoPermission(client):
    url = reverse('no_permission')
    response = client.get(url)
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Brak uprawnień"
    assert response.status_code == 302


@pytest.mark.django_db
def test_EditUser(client, user_in_admin_group):
    user = User.objects.last()
    url = reverse("edit_user", kwargs={"slug": user.slug})
    response = client.get(url)
    assert response.status_code == 302
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_ResetPassword(client, user_in_admin_group):
    user = User.objects.last()
    url = reverse("reset_password", kwargs={"slug": user.slug})
    client.force_login(user)
    response = client.get(url)
    assert response.status_code == 200
    user_without_permissions = User.objects.create_user(
        first_name="first_name2",
        last_name="last_name2",
        username="test@test.pl2",
        password='password', )
    url = reverse("reset_password", kwargs={"slug": user_without_permissions.slug})
    client.force_login(user)
    response = client.post(url, {'password': 'password2',
                                 'password2': 'password2',})
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Hasło zmienione"

@pytest.mark.django_db
def test_about(client):
    url = reverse("about")
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url)
    assert response.status_code == 405
