from django.urls import path
from mainapp.views import ArticleListView

urlpatterns = [
    path('', ArticleListView.as_view(), name='list_articles'),
    path('<slug:slug>', ArticleListView.as_view(), name='category_articles'),
]
