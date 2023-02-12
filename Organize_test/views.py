from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views import View

from Organize_test.models import OrganiseTest
from Test_manager.models import QuestionTest
from Organize_test.forms import OrganizeTestForm, SolveTestForm


# Create your views here.
class OrganizeTest(View):
    def get(self, request):
        form = OrganizeTestForm()
        return render(request, 'organize_test.html', context={"form":form})

    def post(self, request):
        form = OrganizeTestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Test zaplanowany")
            return redirect(reverse("organize_test"))
        messages.error(request, "Błąd")
        return render(request, 'organize_test.html', context={"form":form})


class TestForUserList(View):
    def get(self, request):
        user_league = request.user.league
        test_for_this_league = OrganiseTest.objects.filter(test_for_league=user_league.id)
        return render(request, 'solve_test.html', context={"tests": test_for_this_league})


class SpecificTestToSolve(View):
    def get(self, request, slug):
        test_from_list = OrganiseTest.objects.get(slug=slug)
        selected_test = QuestionTest.objects.filter(test_id=test_from_list.test_number.test_id)
        return render(request, "specific_test_solve.html", context={"test": selected_test})
