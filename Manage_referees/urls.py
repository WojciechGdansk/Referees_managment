"""Manage_referees URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Question_manager import views as quest
from Test_manager import views as test
from User_manager import views as user
from Organization_test import views as orga

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', user.MainPage.as_view(), name="main_page"),
    path('signup/', user.SignUp.as_view(), name='sign_up'),
    path('login/', user.Login.as_view(), name='login'),
    path('manage_users/', user.ManageUsers.as_view(), name="manage_users"),
    path('manage_group/', user.ManageGroups.as_view(), name='manage_groups'),
    path('questions/', quest.QuestionTable.as_view(), name="all_questions"),
    path('create_question/', quest.CreateQuestion.as_view(), name='create_question'),
    path('create_test/', test.CreateTest.as_view(), name="create_test"),
    path('edit_test/<slug:slug>', test.EditTest.as_view(), name="edit_test"),
    path('delete_test/<slug:slug>', test.DeleteTest.as_view(), name="delete_test"),
    path('logout/', user.Logout.as_view(), name="logout"),
    path('group/<int:id>', user.GroupDetails.as_view(), name="group_details"),
    path('browse_tests/', test.DisplayAllTest.as_view(), name="browse_tests"),
    path('test_details2/<slug:slug>', test.TestDetails.as_view(), name="test_detail_other"),
    path('add_question_to_test/<slug:testslug>/<slug:questionslug>', test.AddQuestionToTest.as_view(), name="add_question_to_test"),
    path('edit_question/<slug:slug>', quest.EditQuestion.as_view(), name="edit_question"),
    path('delete_question/<slug:slug>', quest.DeleteQuesiton.as_view(), name="delete_question"),
    path('remove_question_from_test/<slug:slug>/<int:id>', test.RemoveQuestionFromTest.as_view(), name="remove_question_from_test"),
    path('no_permission/', user.NoPermission.as_view(), name="no_permission"),
    path('edit_user/<slug:slug>', user.EditUser.as_view(), name="edit_user"),
    path('reset_password/<slug:slug>', user.ResetPassword.as_view(), name="reset_password"),
    path('organize_test/', orga.OrganizeTest.as_view(), name="organize_test"),
    path('test_solving/', orga.TestForUserList.as_view(), name="test_solving"),
    path('specific_test_solve/<slug:slug>', orga.SpecificTestToSolve.as_view(), name="specific_test_solve"),
    path('result_of_test/<slug:slug>', orga.SpecificTestSolved.as_view(), name="result_of_test"),
    path('history_of_tests/', orga.UserHistoryOfTests.as_view(), name="user_history"),
    path('all_tests_to_check/', orga.DisplayAllTests.as_view(), name="all_tests_to_check"),
    path('specific_test_to_check/<slug:testslug>/<slug:userslug>', orga.CheckSpecificUserTest.as_view(), name="specific_test_to_check"),
    path('stats', orga.Statistics.as_view(), name="statistics"),
    path('about', user.About.as_view(), name="about"),
    path('answers_managment', quest.ManageQuestionsAnswers.as_view(), name="answers_managment"),
    path('add_answer', quest.AddAnswer.as_view(), name="add_answer"),
    path('test_details/<slug:slug>', test.TestDetailsOther.as_view(), name="test_detail"),
    path('test_details3/<slug:slug>', test.TestDetailsOtherJson.as_view(), name="test_detail_other_json"),
    path('questions_not_in_test/<slug:slug>', test.QuestionsNotInTest.as_view(), name="question_not_in_test_json"),
]
