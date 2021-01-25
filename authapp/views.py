from django.urls import reverse_lazy
from django.views.generic import CreateView

from authapp.forms import HabrUserRegisterForm
from authapp.models import HabrUser


class UserRegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации перенаправляет пользователя на главную страницу.
    """
    form_class = HabrUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('list_articles')
    model = HabrUser
