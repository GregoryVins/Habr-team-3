from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView

from authapp.forms import HabrUserRegisterForm, HabrUserLoginForm
from authapp.models import HabrUser


class UserRegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации перенаправляет пользователя на страницу входа.
    """
    form_class = HabrUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('user_login')
    model = HabrUser


class UserLoginView(FormView):
    """
    Авторизация пользователя.
    После успешной авторизации перенаправляет пользователя на главную страницу.
    """
    form_class = HabrUserLoginForm
    template_name = 'authapp/login.html'
    success_url = reverse_lazy('list_articles')

    def form_valid(self, form):
        username = self.request.POST['username']
        password = self.request.POST['password']
        print(username, password)
        userauth = authenticate(self.request, username=username, password=password)
        print(userauth)
        if userauth is not None:
            if userauth.is_active:
                login(self.request, userauth)
        return super(UserLoginView, self).form_valid(form)
