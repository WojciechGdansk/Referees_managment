from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.contrib.auth.models import Group, Permission
from User_manager.forms import SignUpForm, LoginForm, CreateGroupForm
from Test_manager.models import League
from User_manager.models import User


# Create your views here.
class MainPage(View):
    def get(self, request):
        return render(request, 'index.html')


class SignUp(View):
    def get(self, request):
        form = SignUpForm()
        context = {"form": form,
                   "league": League.objects.exclude(which_league="Wszystkie")}
        return render(request, "signup.html", context)

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            league = request.POST.get("league2")
            league_from_base = get_object_or_404(League, slug=league)
            newuser = User.objects.create_user(
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                phone_number=data.get("phone_number"),
                username=data.get('username'),
                password=data.get('password'),
                league=league_from_base)
            messages.success(request, "Pomyślnie utworzono konto")
            try:
                grup = Group.objects.get(name="Sędziowie")
                grup.user_set.add(newuser)
                messages.success(request, "Dodano do grupy sędziowie")
            except:
                messages.info(request, "Nie dodano do grupy")
            return redirect(reverse('main_page'))
        context = {"form": form,
                   "league": League.objects.all()}
        return render(request, "signup.html", context)


class Login(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data.get('email')
            password = data.get('password')
            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                messages.info(request, "Zalogowano")
                return redirect('/')
            else:
                messages.error(request, "Błąd")
                return redirect('/login/')
        return render(request, 'login.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Wylogowano")
        return redirect(reverse('main_page'))


class ManageUsers(View):
    def get(self, request):
        users = User.objects.all()
        groups = Group.objects.all()
        context = {"users": users,
                   "grups": groups}
        return render(request, 'manage_users.html', context)


class ManageGroups(View):
    def get(self, request):
        form = CreateGroupForm()
        context = {"grop": Group.objects.all(),
                   "form": form}
        return render(request, 'manage_group.html', context)

    def post(self, request):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data.get("name")
            Group.objects.create(name=name)
            messages.success(request, "Utworzono nową grupę")
            return redirect(request, '/manage_group/')
            # return redirect(reverse('NAME z URL'))
        context = {"grop": Group.objects.all(),
                   "form": form}
        return render(request, 'manage_group.html', context)


class GroupDetails(View):
    def get(self, request, id):
        grup = get_object_or_404(Group, id=id)
        permission = Permission.objects.all()
        context = {"grup": grup,
                   "permission": permission}
        return render(request, "group_details.html", context)
