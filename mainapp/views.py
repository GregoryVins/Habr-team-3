from django.views.generic import ListView, DetailView

from mainapp.models import Category, Article


class ArticleListView(ListView):
    model = Article
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
