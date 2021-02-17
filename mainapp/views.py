from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.list import MultipleObjectMixin

from mainapp.forms import CommentForm
from mainapp.models import Category, Article, Comment


class ArticleListView(ListView):
    """Отображение всех статей на главной странице с статусом Опубликовано."""
    queryset = Article.objects.filter(status='published', is_banned=False).order_by('-created_at')
    template_name = 'mainapp/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


class ArticleDetailView(DetailView):
    """Детальное отображение конкретной статьи."""
    model = Article
    template_name = 'mainapp/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()

        # Проверка, поставил ли текущий пользователь "лайк" статье.
        article = self.get_object()
        if self.request.user in article.liked_by.all():
            context['user_add_like'] = True
        else:
            context['user_add_like'] = False

        return context


class CategoryDetailView(DetailView, MultipleObjectMixin):
    """Отображение опубликованных статей конкретной категории."""
    model = Category
    template_name = 'mainapp/index.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        object_list = Article.objects.filter(
            category__slug=self.kwargs['slug'], status='published', is_banned=False).order_by('-created_at')
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['categories_list'] = Category.objects.all()
        return context


class CreateCommentView(CreateView):
    """Создание комментариев."""
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        article = Article.objects.get(id=self.kwargs['pk'])
        return reverse('detail_article', kwargs={'slug': article.slug})

    def form_invalid(self, form):
        return HttpResponseRedirect(self.get_success_url())

    def form_valid(self, form):
        article = Article.objects.get(id=self.kwargs['pk'])
        form = form.save(commit=False)
        form.user = self.request.user
        form.article = article
        if self.request.POST.get("parent", None):
            form.parent_id = int(self.request.POST.get("parent"))
        return super().form_valid(form)


class DeleteCommentView(DeleteView):
    """Удаление комментариев."""
    model = Comment

    def get_success_url(self):
        article = self.object.article
        return reverse('detail_article', kwargs={'slug': article.slug})

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class BannedArticleView(UpdateView):
    model = Article
    template_name = 'mainapp/banned_success.html'
    fields = ('is_banned',)

    def get_object(self, queryset=None):
        obj = super().get_object()
        obj.is_banned = True
        obj.save()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context
