from django.urls import path
from mainapp.views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', ArticleListView.as_view(), name='list_articles'),
    path('category/<slug:slug>', ArticleListView.as_view(), name='category_articles'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='detail_article'),
]
