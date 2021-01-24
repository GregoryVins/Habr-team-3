from django.views.generic import CreateView

from authapp.forms import ShopUserRegisterForm
from authapp.models import HabrUser


class UserRegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации перенаправляет пользователя на главную страницу.
    """
    form_class = ShopUserRegisterForm
    template_name = 'authapp/register.html'
    success_url = '/'
    model = HabrUser
