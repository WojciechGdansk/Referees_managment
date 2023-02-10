from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.models import Group, Permission
from User_manager.forms import SignUpForm, LoginForm, CreateGroupForm, EditUserForm, ResetPasswordForm
from Test_manager.models import League
from User_manager.models import User
from django.db.utils import IntegrityError


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
    """View to log in, check validations and return error message when data is incorrect"""
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
                messages.error(request, "Użytkonik nie istnieje bądź podano złe hasło")
                return redirect('/login/')
        return render(request, 'login.html', {'form': form})


class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Wylogowano")
        return redirect(reverse('main_page'))


class ManageUsers(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')
    def test_func(self):
        return self.request.user.groups.filter(name__in=["admin", "Organizator"]).exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request):
        users = User.objects.order_by('league', 'last_name')
        groups = Group.objects.all()
        context = {"users": users,
                   "grups": groups}
        return render(request, 'manage_users.html', context)


class ManageGroups(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

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


class GroupDetails(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="admin").exists()

    def handle_no_permission(self):
        return redirect(reverse("no_permission"))

    def get(self, request, id):
        grup = get_object_or_404(Group, id=id)
        permission = Permission.objects.all()
        context = {"grup": grup,
                   "permission": permission}
        return render(request, "group_details.html", context)


class NoPermission(View):
    """The only purpose of this view is to display message to user who tries to enter view
    without valid permission and redirect to main page"""

    def get(self, request):
        messages.error(request, "Brak uprawnień")
        return redirect(reverse("main_page"))


class EditUser(View):
    """Everyuser can edit self information, users with permissions can manage others"""

    def get(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        leagues = League.objects.all()
        initial_data = {
            "first_name": user.first_name,
            'last_name': user.last_name,
            'phone_number': user.phone_number,
            'username': user.username,
        }
        form = EditUserForm(initial_data)
        groups = Group.objects.order_by('name').exclude(name='admin')
        usergroup = user.groups.order_by('name').exclude(name="admin")
        context = {"form": form,
                   'all_leagues': leagues,
                   'league': user.league,
                   'edited_user': user,
                   'is_active': user.is_active,
                   'groups': groups,
                   'usergroup': usergroup}
        return render(request, "edit_user.html", context)

    def post(self, request, slug):
        user = get_object_or_404(User, slug=slug)
        form = EditUserForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user.first_name = data.get('first_name')
                user.last_name = data.get('last_name')
                user.username = data.get('username')
                user.phone_number = data.get('phone_number')
                is_active = request.POST.get("is_active")
                if is_active == "on":
                    user.is_active = True
                else:
                    user.is_active = False
                league_from_form = request.POST.get("league2")
                group = request.POST.getlist('group')
                for item in user.groups.all():  # setting groups for user
                    if item not in group:
                        user.groups.remove(item)
                for item in group:
                    grup = Group.objects.get(name=item)
                    grup.user_set.add(user)
                user.league = get_object_or_404(League, slug=league_from_form)
                user.save()
                messages.success(request, "Zaktualizowanno")
                return redirect(reverse('main_page'))
            except IntegrityError:
                messages.error(request, "Taki użytkownik już istnieje")
                return render(request, "edit_user.html", context={"form": form})
        return render(request, "edit_user.html", context={"form": form})


class ResetPassword(View):
    """View allows to set new password for user"""

    def get(self, request, slug):
        form = ResetPasswordForm()
        user = get_object_or_404(User, slug=slug)
        return render(request, "reset_password.html", context={
            'form': form,
        })

    def post(self, request, slug):
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            password = data.get('password')
            user = get_object_or_404(User, slug=slug)
            user.set_password(password)
            user.save()
            messages.success(request, "Hasło zmienione")
            return redirect(reverse('main_page'))
        messages.error(request, "Bład")
        return render(request, "reset_password.html", context={'form': form, })
