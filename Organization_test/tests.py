from datetime import datetime

import pytest
from django.test import Client
from django.shortcuts import reverse

from Organization_test.models import OrganiseTest, UserSolving, UserTestResult
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
def test_organize_test(client, user_in_admin_group):
    url = reverse('organize_test')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
    url = reverse('login')
    client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    url = reverse('organize_test')
    response = client.get(url)
    assert response.status_code == 200
    assert OrganiseTest.objects.all().count() == 0
    league = League.objects.create(which_league="testowa liga")
    test_number = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    date_time_to_add = '2023-02-28'
    date_obj = datetime.strptime(date_time_to_add, "%Y-%m-%d").date()
    client.post(url, {'test_for_league': league, 'test_number': test_number, "date_time": date_obj})
    # assert OrganiseTest.objects.all().count() == 1


@pytest.mark.django_db
def test_for_user_list(client, user_in_admin_group):
    url = reverse('test_solving')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/login/?next=/test_solving/'


@pytest.mark.django_db
def test_specific_test_to_solve(client, user_in_admin_group):
    url = reverse('login')
    client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    league = League.objects.create(which_league="testowa liga")
    test_in_alltest = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    date_time_to_add = '2023-02-28'
    date_obj = datetime.strptime(date_time_to_add, "%Y-%m-%d").date()
    OrganiseTest.objects.create(test_for_league=league, test_number=test_in_alltest, date_time=date_obj)
    organise = OrganiseTest.objects.first()
    url = reverse('specific_test_solve', kwargs={'slug': organise.slug})
    response = client.get(url)
    assert OrganiseTest.objects.all().count() == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_SpecificTestSolved(client, user_in_admin_group):
    league = League.objects.create(which_league="testowa liga")
    test_in_alltest = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    date_time_to_add = '2023-02-28'
    date_obj = datetime.strptime(date_time_to_add, "%Y-%m-%d").date()
    OrganiseTest.objects.create(test_for_league=league, test_number=test_in_alltest, date_time=date_obj)
    organise = OrganiseTest.objects.first()
    user = User.objects.first()
    question_object = Questions.objects.create(add_question="A", question_possible_answer="B",
                                               question_correct_answer="C",
                                               for_league="D", added_by=user)
    question_test = QuestionTest.objects.create(test=test_in_alltest, question=question_object)

    user_solved = UserSolving.objects.create(user=user, test_number=test_in_alltest, question=question_test,
                                             user_response="ABC", result=1)
    url = reverse('login')
    client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    url = reverse('result_of_test', kwargs={'slug': organise.slug})
    response = client.get(url)
    assert OrganiseTest.objects.all().count() == 1
    assert UserTestResult.objects.all().count() == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_UserHistoryOfTests(client, user_in_admin_group):
    url = reverse('login')
    client.post(url, {'email': 'test@test.pl', 'password': 'password'})
    url = reverse('user_history')
    response = client.get(url)
    assert response.status_code == 200
    response = client.post(url)
    assert response.status_code == 405


@pytest.mark.django_db
def test_DisplayAllTests(client, user_in_admin_group):
    url = reverse('all_tests_to_check')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'


@pytest.mark.django_db
def test_CheckSpecificUserTest(client, user_in_admin_group):
    league = League.objects.create(which_league="testowa liga")
    test_in_alltest = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    user = User.objects.first()
    url = reverse('specific_test_to_check', kwargs={'testslug': test_in_alltest.slug, "userslug": user.slug})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'


@pytest.mark.django_db
def test_Statistics(client, user_in_admin_group):
    user = User.objects.first()
    question_object = Questions.objects.create(add_question="A", question_possible_answer="B",
                                               question_correct_answer="C",
                                               for_league="D", added_by=user)
    league = League.objects.create(which_league="testowa liga")
    test_in_alltest = AllTest.objects.create(test_name="test", date="2023-05-05", for_league=league)
    url = reverse('statistics')
    response = client.get(url)
    assert AllTest.objects.all().count() == 1
    assert Questions.objects.all().count() == 1
