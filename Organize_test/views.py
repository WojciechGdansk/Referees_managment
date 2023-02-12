from django.shortcuts import render
from django.views import View

from Organize_test.forms import OrganizeTestForm


# Create your views here.
class OrganizeTest(View):
    def get(self, request):
        form = OrganizeTestForm()
        return render(request, 'organize_test.html', context={"form":form})