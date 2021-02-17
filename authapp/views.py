from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DetailView, ListView

from authapp.forms import HabrUserRegisterForm, HabrUserUpdateForm, UserCreateArticleForm, UserUpdateArticleForm
from authapp.models import HabrUser
from mainapp.models import Category, Article


class UserLoginView(LoginView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


class UserRegisterView(CreateView):
    """
    Регистрация пользователя.
    После успешной регистрации перенаправляет пользователя на страницу входа.
    """
    form_class = HabrUserRegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')
    model = HabrUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


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
    paginate_by = 5

    def get_queryset(self):
        user = self.request.user
        queryset = Article.objects.filter(user=user).exclude(status='hidden').order_by('-created_at')
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
        if self.request.method == 'POST':
            if self.request.POST['type'] == 'Сохранить':
                form.instance.status = 'draft'
            elif self.request.POST['type'] == 'Опубликовать':
                form.instance.status = 'moderation'
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

    def get_success_url(self):
        if self.request.POST['type'] == 'Удалить':
            self.success_url = reverse_lazy('user_articles')
        return super().get_success_url()

    def form_valid(self, form):
        if self.request.method == 'POST':
            if self.request.POST['type'] == 'Сохранить':
                form.instance.status = 'draft'
            elif self.request.POST['type'] == 'Опубликовать':
                form.instance.status = 'moderation'
            elif self.request.POST['type'] == 'Удалить':
                form.instance.status = 'hidden'
        return super().form_valid(form)


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
        obj.status = 'draft'
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


# class AddLikeView(View):
#     """
#     Добавление "лайка".
#     Удаление в случае, если "лайк" уже существует.
#     """
#     def get(self, request, *args, **kwargs):
#         article = Article.objects.get(pk=self.kwargs['pk'])
#         if request.user in article.liked_by.all():
#             article.liked_by.remove(request.user)
#             return HttpResponseRedirect(article.get_absolute_url())
#         article.liked_by.add(request.user)
#         return HttpResponseRedirect(article.get_absolute_url())


class AddLikeView(View):
    """
    Добавление "лайка".
    Удаление в случае, если "лайк" уже существует.
    """
    def get(self, request, *args, **kwargs):
        article = Article.objects.get(pk=self.kwargs['pk'])
        try:
            if request.user in article.liked_by.all():
                article.liked_by.remove(request.user)
                user_add_like = 'false'
            else:
                article.liked_by.add(request.user)
                user_add_like = 'true'
        except:
            return JsonResponse({'success': False}, status=400)
        
        likes_info = {
            'likes_count': article.liked_by.count(),
            'user_add_like': user_add_like
        }
        return JsonResponse({'likes_info': likes_info}, status=200)
