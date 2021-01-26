from django.urls import path
from authapp.views import UserRegisterView, UserUpdateView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('update/<int:pk>', UserUpdateView.as_view(), name='user_update'),
]
