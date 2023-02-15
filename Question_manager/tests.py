from django.test import TestCase, Client
import pytest
from django.shortcuts import reverse, redirect

from Question_manager.models import AllPossibleAnswers
from Test_manager.models import Questions
from User_manager.models import User, League
from django.contrib.auth.models import Group, Permission


# Create your tests here.
@pytest.fixture
def client():
    return Client()


@pytest.fixture
def create_user():
    User.objects.create_user(
        first_name="first_name",
        last_name="last_name",
        username="test@test.pl",
        password='password', )


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
def test_QuestionTable_view(client, user_in_admin_group):
    url = reverse('all_questions')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
    url = reverse('login')
    client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    url = reverse('all_questions')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_CreateQuestion_view(client, user_in_admin_group):
    url = reverse('create_question')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
    url = reverse('login')
    client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    url = reverse("create_question")
    response = client.get(url)
    assert response.status_code == 200
    assert Questions.objects.all().count() == 0
    AllPossibleAnswers.objects.create(all_kind_answers="Test")
    League.objects.create(which_league="testowa liga")
    assert League.objects.all().count() == 1
    assert AllPossibleAnswers.objects.all().count() == 1
    client.post(url, data={"add_question": "testowe pytanie",
                      "possible_answer": "1",
                      "correct_answer": "1",
                      "for_league": "1",
                      "added_by": User.objects.first()})
    # assert Questions.objects.all().count() == 1

# @pytest.mark.django_db
# def test_EditQuestion_view(client, user_in_admin_group):
#     url = reverse('edit_question', "some_slug")
#     response = client.get(url)
#     assert response.status_code == 302
#     assert response.url == '/no_permission/'
#     url = reverse('login')
#     client.post(url, {'email': 'test@test.pl', 'password': 'password'})
#     url = reverse("create_question")
#     response = client.get(url)
#     assert response.status_code == 200


# @pytest.mark.django_db
# def test_DeleteQuesiton(client):
#     url = reverse('delete_question')
#     response = client.get(url)
#     assert response.status_code == 302
#     assert response.url == '/no_permission/'