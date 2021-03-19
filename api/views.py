from rest_framework import generics

from .models import Client
from .serializers import ClientSerializer


class ListOrCreateClient(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class RetrieveOrUpdateClient(generics.RetrieveUpdateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'registration_email'
