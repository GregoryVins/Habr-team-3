from django.views.generic import ListView, DetailView

from mainapp.models import Category, Article


class ArticleListView(ListView):
    """Отображение всех опубликованных статей на главной странице."""
    queryset = Article.objects.filter(status='published').order_by('-created_at')
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'

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
        return context


class CategoryDetailView(DetailView):
    """Отображение опубликованных статей конкретной категории."""
    model = Category
    template_name = 'mainapp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_list'] = Category.objects.all()
        context['articles'] = Article.objects.filter(
            category__slug=self.kwargs['slug'], status='published').order_by('-created_at')
        return context
