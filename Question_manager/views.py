from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.contrib import messages
from Question_manager.forms import AddQuestionForm
from Question_manager.models import AllPossibleAnswers
from Test_manager.models import AllTest, Questions, League
from User_manager.models import User


# Create your views here.
class QuestionTable(View):
    def get(self, request):
        all_questions = Questions.objects.all()
        correct_answer = AllPossibleAnswers.objects.all()
        league = League.objects.all()
        context = {'questions': all_questions,
                   "answers": correct_answer,
                   "league": league,
                   "tests": AllTest.objects.all()}
        return render(request, 'all_questions.html', context)


class CreateQuestion(View):
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
            question_possible_answer = request.POST.getlist("possible_answer")
            question_correct_answer = request.POST.getlist("correct_answer")
            for_league = request.POST.getlist("for_league")
            user = User.objects.get(id=request.user.id)
            Questions.objects.create(add_question=add_question, question_possible_answer=question_possible_answer,
                                     question_correct_answer=question_correct_answer,
                                     for_league=for_league, added_by=user)
            messages.info(request, "Pytanie dodane poprawnie")
            return redirect("/")
        return render(request, "add_question.html", context)


class EditQuestion(View):
    def get(self, request, slug):
        question = get_object_or_404(Questions, slug=slug)
        form = AddQuestionForm()
        context = {"question": question,
                   "form": form}
        return render(request, "edit_question.html", context)


class DeleteQuesiton(View):
    """View removes specific question from questions base"""

    def get(self, request, slug):
        question = get_object_or_404(Questions, slug=slug)
        question.delete()
        messages.success(request, "Pytanie usunięte")
        return redirect(reverse('all_questions'))
