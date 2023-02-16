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
    user = User.objects.last()
    client.force_login(user)
    url = reverse("create_question")
    response = client.get(url)
    assert response.status_code == 200
    assert Questions.objects.all().count() == 0
    AllPossibleAnswers.objects.create(all_kind_answers="Test2")
    league = League.objects.create(which_league="testowa liga5")
    league_id = League.objects.first().id
    assert League.objects.all().count() == 1
    assert AllPossibleAnswers.objects.all().count() == 1
    r = client.post(url, data={"add_question": "testowe pytanie555",
                           'question_possible_answer': ['1'],
                           'question_correct_answer': ['1'],
                           'for_league': [league_id]
                           })
    assert Questions.objects.count() == 1

@pytest.mark.django_db
def test_EditQuestion_view(client, user_in_admin_group):
    user = User.objects.last()
    client.force_login(user)
    url = reverse("create_question")
    response = client.get(url)
    assert response.status_code == 200
    assert Questions.objects.all().count() == 0
    AllPossibleAnswers.objects.create(all_kind_answers="Test10")
    answers_id = AllPossibleAnswers.objects.last().id
    league = League.objects.create(which_league="testowa liga10")
    league_id = League.objects.first().id
    assert League.objects.all().count() == 1
    assert AllPossibleAnswers.objects.all().count() == 1
    client.post(url, data={"add_question": "testowe pytanie99",
                           'question_possible_answer': [answers_id],
                           'question_correct_answer': [answers_id],
                           'for_league': [league_id]
                           })

    assert Questions.objects.count() == 1
    question = Questions.objects.last()
    url = reverse("edit_question", kwargs={"slug": question.slug})
    response = client.get(url)
    assert response.status_code == 200
    client.post(url, data={"add_question": "testowe pytanie2",
                           'question_possible_answer': [answers_id],
                           'question_correct_answer': [answers_id],
                           'for_league': [league_id]
                           })
    assert Questions.objects.last().add_question == "testowe pytanie2"


@pytest.mark.django_db
def test_DeleteQuesiton(client, user_in_admin_group):
    user = User.objects.last()
    client.force_login(user)
    url = reverse("create_question")
    response = client.get(url)
    assert response.status_code == 200
    assert Questions.objects.all().count() == 0
    AllPossibleAnswers.objects.create(all_kind_answers="Test456789")
    answers_id = AllPossibleAnswers.objects.last().id
    league = League.objects.create(which_league="testowa liga12345")
    league_id = League.objects.first().id
    assert League.objects.all().count() == 1
    assert AllPossibleAnswers.objects.all().count() == 1
    client.post(url, data={"add_question": "testowe pytanie",
                           'question_possible_answer': [answers_id ],
                           'question_correct_answer': [answers_id ],
                           'for_league': [league_id]
                           })

    assert Questions.objects.count() == 1
    question = Questions.objects.last()
    url = reverse("delete_question", kwargs={"slug": question.slug})
    response = client.get(url)
    assert response.status_code == 302
    assert Questions.objects.count() == 0

