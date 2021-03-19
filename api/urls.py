from django.urls import path

from .views import ListOrCreateClient, RetrieveOrUpdateClient

urlpatterns = [
    path('', ListOrCreateClient.as_view()),
    path('client/<str:registration_email>/', RetrieveOrUpdateClient.as_view()),
]
