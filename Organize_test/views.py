from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from django.views import View

from Organize_test.forms import OrganizeTestForm


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