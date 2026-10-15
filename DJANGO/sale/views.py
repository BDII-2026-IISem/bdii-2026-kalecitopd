from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import Sale, SaleDetail
from .serializers import SaleSerializer, SaleDetailSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

class SaleDetailViewSet(viewsets.ModelViewSet):
    queryset = SaleDetail.objects.all()
    serializer_class = SaleDetailSerializer