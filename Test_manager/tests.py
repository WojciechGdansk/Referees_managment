import pytest
from django.contrib.messages import get_messages
from django.test import Client
from django.shortcuts import reverse

from Test_manager.models import AllTest, Questions, QuestionTest
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
def test_CreateTest(client, user_in_admin_group):
    user = User.objects.first()
    client.force_login(user)
    url = reverse('create_test')
    response = client.get(url)
    assert response.status_code == 200
    league = League.objects.create(which_league="test")
    league = League.objects.last()
    data = {"test_name": "testowy test",
            "date": "2023-05-05",
            "for_league": league.id
            }
    response = client.post(url, data)
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Dodano test"
    assert response.status_code == 302
    assert AllTest.objects.all().count() == 1

@pytest.mark.django_db
def test_DisplayAllTest(client, user_in_admin_group):
    url = reverse('browse_tests')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
    user = User.objects.first()
    client.force_login(user)
    url = reverse('browse_tests')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_TestDetails(client, user_in_admin_group):
    league = League.objects.create(which_league="testowa liga")
    test_number = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    necessary_slug = test_number.slug
    url = reverse('test_detail', kwargs={'slug': necessary_slug})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
    user = User.objects.first()
    client.force_login(user)
    url = reverse('test_detail', kwargs={'slug': necessary_slug})
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_AddQuestionToTest(client, user_in_admin_group):
    user = User.objects.first()
    client.force_login(user)
    league = League.objects.create(which_league="testowa liga")
    test_in_alltest = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    question_object = Questions.objects.create(add_question="A", question_possible_answer="B",
                                               question_correct_answer="C",
                                               for_league="D", added_by=user)
    url = reverse('add_question_to_test', kwargs={'testslug': test_in_alltest.slug, "questionslug": question_object.slug})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('all_questions')
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Pytanie dodane do testu"

@pytest.mark.django_db
def test_RemoveQuestionFromTest(client, user_in_admin_group):
    user = User.objects.first()
    client.force_login(user)
    league = League.objects.create(which_league="testowa liga")
    test_in_alltest = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    question_object = Questions.objects.create(add_question="A", question_possible_answer="B",
                                               question_correct_answer="C",
                                               for_league="D", added_by=user)
    question_test = QuestionTest.objects.create(test=test_in_alltest, question=question_object)
    assert QuestionTest.objects.all().count() == 1
    url = reverse('remove_question_from_test', kwargs={'slug': question_object.slug, "id": question_test.id})
    response = client.get(url)
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Pytanie usunięto z testu"
    assert QuestionTest.objects.all().count() == 0


@pytest.mark.django_db
def test_EditTest(client, user_in_admin_group):
    user = User.objects.first()
    client.force_login(user)
    league = League.objects.create(which_league="testowa liga")
    test_number = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    url = reverse('edit_test', kwargs={"slug": test_number.slug})
    response = client.get(url)
    assert response.status_code == 200
    league = League.objects.last()
    data = {"test_name": "testowy test edycja",
            "date": '2023-05-05',
            "for_league": league.id
            }
    response = client.post(url, data)
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Zaktualizowano test"

@pytest.mark.django_db
def test_DeleteTest(client, user_in_admin_group):
    user = User.objects.first()
    client.force_login(user)
    league = League.objects.create(which_league="testowa liga")
    test_number = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    url = reverse('delete_test', kwargs={"slug": test_number.slug})
    assert AllTest.objects.all().count() == 1
    response = client.get(url)
    assert AllTest.objects.all().count() == 0
    messages = list(get_messages(response.wsgi_request))
    assert str(messages[0]) == "Test usunięty"

