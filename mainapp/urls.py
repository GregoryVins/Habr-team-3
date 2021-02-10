from django.urls import path
from mainapp.views import ArticleListView, ArticleDetailView, CategoryDetailView, CreateCommentView

urlpatterns = [
    path('', ArticleListView.as_view(), name='list_articles'),
    path('article/<slug:slug>/', ArticleDetailView.as_view(), name='detail_article'),
    path('category/<slug:slug>', CategoryDetailView.as_view(), name='category_articles'),
    path('article/comment/<int:pk>/', CreateCommentView.as_view(), name='create_comment'),
]
