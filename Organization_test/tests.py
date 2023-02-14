from datetime import datetime

import pytest
from django.test import TestCase, Client
from django.shortcuts import reverse, redirect

from Organization_test.models import OrganiseTest
from Test_manager.models import AllTest
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

