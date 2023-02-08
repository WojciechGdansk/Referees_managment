from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.views import View
import datetime
from django.contrib import messages
from Test_manager.forms import CreateTestForm
from Test_manager.models import AllTest, League, Questions, QuestionTest
from User_manager.models import User


# Create your views here.
class CreateTest(View):
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
            data = form.cleaned_data
            test_name = data.get('name')
            date = request.POST['date']
            for_league = League.objects.get(id=int(data.get('for_league')))
            user = User.objects.get(id=request.user.id)
            AllTest.objects.create(test_name=test_name, date=date, for_league=for_league, created_by=user)
            messages.success(request, "Dodano test")
            return redirect(reverse("browse_tests"))
        messages.error(request, "Wystąpił błąd")
        return redirect("/")


class DisplayAllTest(View):
    def get(self, request):
        tests = AllTest.objects.all()
        context = {"tests": tests}
        return render(request, "all_tests.html", context)


class TestDetails(View):
    def get(self, request, slug):
        test = AllTest.objects.get(slug=slug)
        filters = [test.for_league, "Wszystkie"]
        questions = Questions.objects.filter(for_league__in=filters)
        question_for_tests = QuestionTest.objects.filter(test_id=test.id)
        context = {"test": test,
                   "questions": questions,
                   "que": question_for_tests}
        return render(request, "test_details.html", context)


class AddQuestionToTest(View):
    def get(self, request, testslug, questionslug):
        question = get_object_or_404(Questions, slug=questionslug)
        test = get_object_or_404(AllTest, slug=testslug)
        question_to_test, exist = QuestionTest.objects.get_or_create(test=test, question=question) #to avoid duplicated questions on one test
        if exist==False:
            messages.info(request, "To pytanie jest już w tym teście")
            return redirect(reverse('all_questions'))
        messages.success(request, "Pytanie dodane do testu")
        return redirect(reverse('browse_tests'))


class RemoveQuestionFromTest(View):
    """View allows user to remove selected question from test"""
    def get(self, request, id, slug):
        questiontest = get_object_or_404(QuestionTest, id=id)
        questiontest.delete()
        messages.success(request, "Pytanie usunięto z testu")
        return redirect(reverse('test_detail', kwargs={'slug': questiontest.test.slug}))