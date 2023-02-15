from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib import messages
from Question_manager.forms import AddQuestionForm
from Question_manager.models import AllPossibleAnswers
from Test_manager.models import AllTest, Questions, League, PossibleAnswers, CorrectAnswer
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
        posibble_answers = PossibleAnswers.objects.all()
        correct_answers = CorrectAnswer.objects.all()

        league = League.objects.all()
        todays_date = datetime.datetime.today()
        todays_date = datetime.datetime.strftime(todays_date, "%Y-%m-%d")
        context = {'questions': all_questions,
                   "answers": posibble_answers,
                   "league": league,
                   "correct_answers": correct_answers,
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
        return render(request, "add_question.html", context = {"form": form})

    def post(self, request):
        form = AddQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.added_by = request.user
            question.save()
            selected_questions_possible_answer = request.POST.getlist('question_possible_answer')
            selected_correct_answers = request.POST.getlist('question_correct_answer')
            for item in selected_questions_possible_answer:
                PossibleAnswers.objects.create(question=question,
                                               question_possible_answers=AllPossibleAnswers.objects.get(id=item))
            for item in selected_correct_answers:
                CorrectAnswer.objects.create(question=question,
                                               question_correct_answers=AllPossibleAnswers.objects.get(id=item))



            messages.info(request, "Pytanie dodane poprawnie")
            return redirect("/")
        return render(request, "add_question.html", context = {"form": form})


class EditQuestion(UserPassesTestMixin, View):
    """View to edit already exisitng question in database"""
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Komisja szkoleniowa", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, slug):
        question = get_object_or_404(Questions, slug=slug)
        form = AddQuestionForm(instance=question)
        context = {"question": question,
                   "form": form}
        return render(request, "edit_question.html", context)

    def post(self, request, slug):
        question = get_object_or_404(Questions, slug=slug)
        form = AddQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.info(request, "Uaktualniono")
            return redirect("/")
        return render(request, "add_question.html", context = {"form": form})


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
