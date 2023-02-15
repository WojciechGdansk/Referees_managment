
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, reverse
from django.views import View

from Organization_test.models import OrganiseTest, UserSolving, UserTestResult
from Test_manager.models import QuestionTest, AllTest, PossibleAnswers, Questions, CorrectAnswer
from User_manager.models import User
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
        if request.user.is_superuser:
            return render(request, 'solve_test.html', context={"tests": OrganiseTest.objects.all()})
        user_league = request.user.league
        test_for_this_league = OrganiseTest.objects.filter(test_for_league=user_league.id)
        tests_done_for_this_league = [item.test_number_id for item in test_for_this_league]
        # returns object which has been created when user done test
        check_if_user_solved_this_test = UserSolving.objects.filter(test_number_id__in=tests_done_for_this_league,
                                                                    user_id=request.user.id)

        #tests number done by user
        test_done_by_user_for_this_league = set()
        for item in check_if_user_solved_this_test:
            test_done_by_user_for_this_league.add(item.test_number_id)
        #all test for this league
        all_test_numbers_for_this_league = set()
        for item in test_for_this_league:
            all_test_numbers_for_this_league.add(item.test_number_id)

        #tests not done by user
        test_not_done_by_user = list(all_test_numbers_for_this_league.difference(test_done_by_user_for_this_league))
        test_for_this_league = OrganiseTest.objects.filter(test_for_league=user_league.id,
                                                           test_number__in=test_not_done_by_user)

        #users with perms can see all tests prepared to solve
        if test_for_this_league is False and not request.user.has_perm("Test_manager.view_alltest"):
            return render(request, 'solve_test.html')
        if request.user.has_perm("Test_manager.view_alltest"):
            return render(request, 'solve_test.html', context={"tests": OrganiseTest.objects.all()})
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
        possible_answers = PossibleAnswers.objects.all()
        return render(request, "specific_test_solve.html", context={"test": selected_test,
                                                                    "possible_answer": possible_answers,
                                                                    "user": request.user})

    def post(self, request, slug):
        user = request.user
        test_number = OrganiseTest.objects.get(slug=slug)
        test_from_database = AllTest.objects.get(id=test_number.test_number.id)
        questions = QuestionTest.objects.filter(test_id=test_number.test_number.id)
        for item in questions:
            user_response = request.POST.getlist(item.question.slug) #user answer
            correct_answer = [] #correct answer for question from test
            for answer in CorrectAnswer.objects.all():
                if answer.question.slug == item.question.slug:
                    correct_answer.append(answer.question_correct_answers.all_kind_answers)
            if user_response == correct_answer:
                result = 1
            elif user_response + ["+"] == correct_answer:
                result = 0.5
            elif user_response == correct_answer + ["+"]:
                result = 0.5
            else:
                result = 0
            UserSolving.objects.create(
                user=user,
                test_number=test_from_database,
                question=item,
                user_response=user_response,
                result=result)
        return redirect(reverse('result_of_test', kwargs={'slug': test_number.slug}))


class SpecificTestSolved(LoginRequiredMixin, View):
    """Adds info about result to UserTestResult model, present user result of test"""

    def get(self, request, slug):
        test_from_list = OrganiseTest.objects.get(slug=slug)
        which_test = UserSolving.objects.filter(test_number=test_from_list.test_number.id).filter(user=request.user)
        correct_answers = CorrectAnswer.objects.all()
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
                                                                     "result": final_result,
                                                                     "correct": correct_answers})


class UserHistoryOfTests(LoginRequiredMixin, View):
    """Allows user to check history of tests, check specific test"""

    def get(self, request):
        user_tests = UserTestResult.objects.filter(user=request.user)
        return render(request, 'user_test_history.html', context={
            "tests": user_tests
        })


class DisplayAllTests(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request):
        user_tests = UserTestResult.objects.all()
        return render(request, "user_tests.html", context={"user_test": user_tests})


class CheckSpecificUserTest(UserPassesTestMixin, View):
    """Restricted view, users who belong to selected group can view tests and results"""
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, testslug, userslug):
        test_from_list = OrganiseTest.objects.get(slug=testslug)
        user_who_solved_test = User.objects.get(slug=userslug)
        which_test = UserSolving.objects.filter(test_number=test_from_list.test_number.id).filter(user=user_who_solved_test)
        result = UserTestResult.objects.get(organise_test_slug=test_from_list)
        correct_answers = CorrectAnswer.objects.all()
        return render(request, "user_test_check.html.html", context={"test": test_from_list,
                                                                     "solution": which_test,
                                                                     "user_solved": user_who_solved_test,
                                                                     'result': result,
                                                                     "correct": correct_answers})

class Statistics(View):
    def get(self, request):
        test_number = AllTest.objects.all().count()
        question_number = Questions.objects.all().count()
        all_results = UserTestResult.objects.all()
        sum_of_points = []
        for item in all_results:
            sum_of_points.append(item.result)
        if len(sum_of_points) != 0:
            average = sum(sum_of_points)/len(sum_of_points)
        else:
            average = 0
        return render(request, "statistics.html", context={
            "test_number": test_number,
            "questions": question_number,
            "average": average
        })