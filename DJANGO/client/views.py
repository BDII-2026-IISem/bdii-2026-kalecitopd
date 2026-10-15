from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from security.permissions import HasResourcePermission
from .models import Client
from .serializers import ClientSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, HasResourcePermission]
    resource_name = 'clients'  # Nombre del recurso con el que validarás permisos

