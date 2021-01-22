from django.views.generic import ListView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'
