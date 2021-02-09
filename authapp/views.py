from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from authapp.forms import HabrUserRegisterForm, HabrUserUpdateForm, UserCreateArticleForm, UserUpdateArticleForm
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


class UserCreateArticleView(CreateView):
    """Создание новой статьи."""
    template_name = 'registration/create_article.html'
    success_url = reverse_lazy('user_articles')
    model = Article
    form_class = UserCreateArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserUpdateArticleView(UpdateView):
    """Редактирвоание статьи."""
    model = Article
    form_class = UserUpdateArticleForm
    template_name = 'registration/create_article.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


class UserRemoveArticleView(UpdateView):
    """
    Снятие статьи с публикации.
    Изменение статуса с Опубликована на Черновик.
    """
    model = Article
    fields = ('status',)
    template_name = 'registration/success_remove.html'

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.status = 'Черновик'
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context
