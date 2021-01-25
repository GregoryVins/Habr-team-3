from django.urls import reverse_lazy
from django.views.generic import CreateView

from authapp.forms import HabrUserRegisterForm
from authapp.models import HabrUser


class UserRegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации перенаправляет пользователя на страницу входа.
    """
    form_class = HabrUserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('user_login')
    model = HabrUser
