from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
import datetime
from django.contrib import messages
from Test_manager.forms import CreateTestForm
from Test_manager.models import AllTest, League, Questions, QuestionTest
from User_manager.models import User


# Create your views here.
class CreateTest(UserPassesTestMixin, View):
    """View to create test, allows to write name of test, select date and for which league,
    created_by filled automatically with User object who was logged in and created test"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request):
        form = CreateTestForm()
        today = datetime.datetime.now()
        today = today.strftime("%Y-%m-%d")
        context = {"form": form,
                   "today": today}
        return render(request, 'create_test.html', context)

    def post(self, request):
        form = CreateTestForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.created_by = request.user
            data.save()
            messages.success(request, "Dodano test")
            return redirect(reverse("browse_tests"))
        messages.error(request, "Wystąpił błąd")
        return redirect(reverse('main_page'))


class DisplayAllTest(UserPassesTestMixin, View):
    """User with rights can browse all existing tests"""
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request):
        tests = AllTest.objects.all()
        context = {"tests": tests}
        return render(request, "all_tests.html", context)


class TestDetails(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, slug):
        test = AllTest.objects.get(slug=slug)
        filters = [test.for_league, "Wszystkie"]
        questions = Questions.objects.filter(for_league__in=filters)
        question_for_tests = QuestionTest.objects.filter(test_id=test.id)
        context = {"test": test,
                   "questions": questions,
                   "que": question_for_tests}
        return render(request, "test_details.html", context)


class AddQuestionToTest(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, testslug, questionslug):
        question = get_object_or_404(Questions, slug=questionslug)
        test = get_object_or_404(AllTest, slug=testslug)
        question_to_test, exist = QuestionTest.objects.get_or_create(test=test,
                                                                     question=question)  # to avoid duplicated questions on one test
        if exist == False:
            messages.info(request, "To pytanie jest już w tym teście")
            return redirect(reverse('all_questions'))
        messages.success(request, "Pytanie dodane do testu")
        return redirect(reverse('all_questions'))


class RemoveQuestionFromTest(UserPassesTestMixin, View):
    """View allows user to remove selected question from test"""

    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, id, slug):
        questiontest = get_object_or_404(QuestionTest, id=id)
        questiontest.delete()
        messages.success(request, "Pytanie usunięto z testu")
        return redirect(reverse('test_detail', kwargs={'slug': questiontest.test.slug}))


class EditTest(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, slug):
        test = get_object_or_404(AllTest, slug=slug)
        form = CreateTestForm(instance=test)
        context = {"form": form}
        return render(request, "edit_test.html", context)

    def post(self, request, slug):
        test = get_object_or_404(AllTest, slug=slug)
        form = CreateTestForm(request.POST, instance=test)
        if form.is_valid():
            form.save()
            messages.success(request, "Zaktualizowano test")
            return redirect(reverse("browse_tests"))
        messages.error(request, "Wystąpił błąd")
        return redirect(reverse('main_page'))


class DeleteTest(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, slug):
        test = get_object_or_404(AllTest, slug=slug)
        test.delete()
        messages.success(request, "Test usunięty")
        return redirect(reverse('browse_tests'))
