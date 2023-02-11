from django.test import TestCase, Client
import pytest
from django.shortcuts import reverse, redirect

from Test_manager.models import Questions
from User_manager.models import User, League


# Create your tests here.
@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
def test_QuestionTable_view(client):
    url = reverse('all_questions')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'


@pytest.mark.django_db
def test_CreateQuestion_view(client):
    url = reverse('create_question')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'


@pytest.mark.django_db
def test_EditQuestion_view(client):
    league = League.objects.create(which_league="test")
    user = User.objects.create_user(
        first_name="first_name",
        last_name="last_name",
        username="test@test.pl",
        password='password', )
    question = Questions.objects.create(add_question="test", question_possible_answer='test',
                                        question_correct_answer='test',
                                        for_league=league, added_by=user)
    url = reverse('edit_question', question.slug)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == '/no_permission/'
