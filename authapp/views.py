from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from authapp.forms import HabrUserRegisterForm, HabrUserUpdateForm
from authapp.models import HabrUser
from mainapp.models import Category


class UserRegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации перенаправляет пользователя на страницу входа.
    """
    form_class = HabrUserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    model = HabrUser


class UserAccountUpdateView(UpdateView):
    """
    Обновление личной информации.
    """
    form_class = HabrUserUpdateForm
    template_name = 'registration/update.html'
    success_url = reverse_lazy('user_update_account')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()

        return context
