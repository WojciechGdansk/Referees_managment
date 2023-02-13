import ast

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, reverse
from django.views import View

from Organization_test.models import OrganiseTest, UserSolving, UserTestResult
from Test_manager.models import QuestionTest, AllTest
from Organization_test.forms import OrganizeTestForm


# Create your views here.
class OrganizeTest(UserPassesTestMixin, View):
    """View used to organize test, select league, date and test to provide users"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request):
        form = OrganizeTestForm()
        return render(request, 'organize_test.html', context={"form": form})

    def post(self, request):
        form = OrganizeTestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Test zaplanowany")
            return redirect(reverse("organize_test"))
        messages.error(request, "Błąd")
        return render(request, 'organize_test.html', context={"form": form})


class TestForUserList(LoginRequiredMixin, View):
    """View show logged user available test to solve, if user already solved test,  it's not on the list"""

    def get(self, request):
        user_league = request.user.league
        test_for_this_league = OrganiseTest.objects.filter(test_for_league=user_league.id)
        tests_done_for_this_league = [item.test_number_id for item in test_for_this_league]
        # check if user already solved this test
        check_if_user_solved_this_test = UserSolving.objects.filter(test_number_id__in=tests_done_for_this_league)
        if check_if_user_solved_this_test:
            return render(request, 'solve_test.html')
        return render(request, 'solve_test.html', context={"tests": test_for_this_league})


class SpecificTestToSolve(LoginRequiredMixin, View):
    """View which let user solve test,
    checks whether user already made this test,
    if so user will be redirected to result of his test.
    View also checks if there are tests available for league for specific user"""

    def get(self, request, slug):
        test_from_list = OrganiseTest.objects.get(slug=slug)
        check_if_user_made_this_test = UserSolving.objects.filter(test_number=test_from_list.test_number,
                                                                  user=request.user.id)
        # check if user already made this test
        if check_if_user_made_this_test:
            return redirect(reverse('result_of_test', kwargs={'slug': test_from_list.slug}))
        selected_test = QuestionTest.objects.filter(test_id=test_from_list.test_number.id)
        return render(request, "specific_test_solve.html", context={"test": selected_test})

    def post(self, request, slug):
        user = request.user
        test_number = OrganiseTest.objects.get(slug=slug)
        test_from_database = AllTest.objects.get(id=test_number.test_number.id)
        questions = QuestionTest.objects.filter(test_id=test_number.test_number.id)
        for item in questions:
            question_from_database = item
            user_response = request.POST.getlist(item.question.slug)
            user_response_splited = [item.split(',') for item in user_response][0]
            user_response_splited = sorted(user_response_splited)
            correct_answer = ast.literal_eval(item.question.question_correct_answer)
            correct_answer = sorted(correct_answer)
            if user_response_splited == correct_answer:
                result = 1
            else:
                result = 0
            UserSolving.objects.create(
                user=user,
                test_number=test_from_database,
                question=question_from_database,
                user_response=user_response,
                result=result)
        return redirect(reverse('result_of_test', kwargs={'slug': test_number.slug}))


class SpecificTestSolved(LoginRequiredMixin, View):
    """Adds info about result to UserTestResult model, present user result of test"""

    def get(self, request, slug):
        test_from_list = OrganiseTest.objects.get(slug=slug)
        which_test = UserSolving.objects.filter(test_number=test_from_list.test_number.id).filter(user=request.user)
        who_solved = which_test[0].user
        final_result = 0
        for res in which_test:
            final_result += res.result
        add_to_model, exists = UserTestResult.objects.get_or_create(
            user=request.user,
            test_number=test_from_list.test_number,
            result=final_result,
            organise_test_slug=test_from_list)
        return render(request, "solved_specific_test.html", context={"test": test_from_list,
                                                                     "solution": which_test,
                                                                     "who_solved": who_solved,
                                                                     "result": final_result})


class UserHistoryOfTests(LoginRequiredMixin, View):
    """Allows user to check history of tests, check specific test"""

    def get(self, request):
        user_tests = UserTestResult.objects.filter(user=request.user)
        return render(request, 'user_test_history.html', context={
            "tests": user_tests
        })
