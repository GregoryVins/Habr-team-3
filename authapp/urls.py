from django.urls import path

from authapp.views import UserRegisterView, UserAccountUpdateView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('update/account/', UserAccountUpdateView.as_view(), name='user_update_account'),
]
