from django.urls import path

from authapp.views import UserLoginView, UserRegisterView, UserAccountUpdateView, UserAccountStatisticView, UserAccountMyArticles, \
    UserCreateArticleView, UserUpdateArticleView, UserRemoveArticleView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('account/', UserAccountStatisticView.as_view(), name='user_statistic'),
    path('account/update/', UserAccountUpdateView.as_view(), name='user_update_data'),
    path('account/articles/', UserAccountMyArticles.as_view(), name='user_articles'),
    path('account/articles/create/', UserCreateArticleView.as_view(), name='user_create_article'),
    path('account/articles/update/<slug:slug>/', UserUpdateArticleView.as_view(), name='user_update_article'),
    path('account/articles/remove/<slug:slug>/', UserRemoveArticleView.as_view(), name='user_remove_article'),
]
