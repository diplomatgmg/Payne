from django.contrib import auth, messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from apps.users.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserChangePasswordForm
from apps.users.models import CustomUser
from mixins.views import TitleMixin


# Create your views here.


class UserLoginView(TitleMixin, LoginView):
    title = 'Вход'
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('index')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not form.is_valid() and form.errors.get('username'):
            user = CustomUser.find_user(form.cleaned_data['username_or_email'], form.cleaned_data['password'])
            if user:
                auth.login(self.request, user)
                return self.form_valid(form)
            messages.error(request, 'Неверное имя пользователя и/или пароль')
        return self.form_invalid(form)



class UserCreateView(TitleMixin, CreateView):
    title = 'Регистрация'
    model = CustomUser
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()
        username, password = self.request.POST['username'], self.request.POST['password1']
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        return redirect(self.success_url)


class ProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    title = 'Профиль'
    model = CustomUser
    template_name = 'users/profile.html'
    form_class = UserProfileForm

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context



class ChangeUserPassword(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    form_class = UserChangePasswordForm
    title = 'Изменение пароля'
    login_url = reverse_lazy('login')

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.id})
