from django.urls import path
from .views import ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='list_articles')
]
