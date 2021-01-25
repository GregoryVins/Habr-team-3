from django.urls import path
from authapp.views import UserRegisterView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user_register'),
]
