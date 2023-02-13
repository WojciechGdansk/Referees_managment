from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib import messages
from Question_manager.forms import AddQuestionForm
from Question_manager.models import AllPossibleAnswers
from Test_manager.models import AllTest, Questions, League
from User_manager.models import User
import datetime


# Create your views here.
class QuestionTable(UserPassesTestMixin, View):
    """View allows to display all existing questions,
    allows to add question to specific test.
    Planned test date must be greater than today"""
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request):
        all_questions = Questions.objects.all()
        correct_answer = AllPossibleAnswers.objects.all()
        league = League.objects.all()
        todays_date = datetime.datetime.today()
        todays_date = datetime.datetime.strftime(todays_date, "%Y-%m-%d")
        context = {'questions': all_questions,
                   "answers": correct_answer,
                   "league": league,
                   "tests": AllTest.objects.filter(date__gte=todays_date)}
        return render(request, 'all_questions.html', context)


class CreateQuestion(UserPassesTestMixin, View):
    """Allows to create question and save to database,
    requires permissions"""
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request):
        form = AddQuestionForm()
        context = {"form": form}
        return render(request, "add_question.html", context)

    def post(self, request):
        form = AddQuestionForm(request.POST)
        context = {"form": form}
        if form.is_valid():
            data = form.cleaned_data
            add_question = data.get('add_question')
            question_possible = request.POST.getlist("possible_answer")
            question_correct = request.POST.getlist("correct_answer")
            league = request.POST.getlist("for_league")
            question_possible_answer = []
            #Add question with normal answer instead of number
            for item in question_possible:
                question_possible_answer.append(AllPossibleAnswers.objects.get(id=int(item)).all_kind_answers)
            question_correct_answer = []
            for item in question_correct:
                question_correct_answer.append(AllPossibleAnswers.objects.get(id=int(item)).all_kind_answers)
            for_league = []
            for item in league:
                for_league.append(League.objects.get(id=int(item)).which_league)
            user = User.objects.get(id=request.user.id)
            Questions.objects.create(add_question=add_question, question_possible_answer=question_possible_answer,
                                     question_correct_answer=question_correct_answer,
                                     for_league=for_league, added_by=user)
            messages.info(request, "Pytanie dodane poprawnie")
            return redirect("/")
        return render(request, "add_question.html", context)


class EditQuestion(UserPassesTestMixin, View):
    """View to edit already exisitng question in database"""
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, slug):
        question = get_object_or_404(Questions, slug=slug)
        #initial to musi byc slownik z kluczami, klucze nazwy pol, wartrosci to te ktore powinny byc
        initial_data = {"add_question": question.add_question}
        form = AddQuestionForm(initial_data)
        context = {"question": question,
                   "form": form}
        return render(request, "edit_question.html", context)


class DeleteQuesiton(UserPassesTestMixin, View):
    """View removes specific question from questions base"""
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, slug):
        question = get_object_or_404(Questions, slug=slug)
        question.delete()
        messages.success(request, "Pytanie usunięte")
        return redirect(reverse('all_questions'))
