from django.views.generic import ListView, DetailView, CreateView

from mainapp.models import Category, Article, Comment
from mainapp.forms import CommentForm

from django.urls import reverse


class ArticleListView(ListView):
    queryset = Article.objects.filter(status='published').order_by('-created_at')
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'mainapp/article_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        context['articles'] = Article.objects.filter(
            category__slug=self.kwargs['slug'], status='published').order_by('-created_at')
        return context


class CreateCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    
    def get_success_url(self):
        article = Article.objects.get(id=self.kwargs['pk'])
        return reverse('detail_article', kwargs={'slug': article.slug})

    def form_valid(self, form):
        article = Article.objects.get(id=self.kwargs['pk'])
        form = form.save(commit=False)
        form.user = self.request.user
        form.article = article
        return super().form_valid(form)
 