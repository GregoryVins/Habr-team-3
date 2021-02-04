from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from authapp.forms import HabrUserRegisterForm, HabrUserUpdateForm
from authapp.models import HabrUser
from mainapp.models import Category, Article


class UserRegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации перенаправляет пользователя на страницу входа.
    """
    form_class = HabrUserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    model = HabrUser


class UserAccountStatisticView(DetailView):
    """Отображение статистики."""
    template_name = 'registration/statistic.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()

        return context


class UserAccountUpdateView(UpdateView):
    """Обновление личной информации."""
    form_class = HabrUserUpdateForm
    template_name = 'registration/update_personal_data.html'
    success_url = reverse_lazy('user_update_data')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()

        return context


class UserAccountMyArticles(ListView):
    """Список всех статей."""
    template_name = 'registration/my_articles.html'
    context_object_name = 'articles'

    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.filter(user=user).order_by('-created_at')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()

        return context
