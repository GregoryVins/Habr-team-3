from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from authapp.forms import HabrUserRegisterForm, HabrUserUpdateForm
from authapp.models import HabrUser


class UserRegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации перенаправляет пользователя на страницу входа.
    """
    form_class = HabrUserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    model = HabrUser


class UserUpdateView(UpdateView):
    """
    Обновление личной информации.
    """
    form_class = HabrUserUpdateForm
    template_name = 'registration/update.html'
    success_url = reverse_lazy('list_articles')
    model = HabrUser

