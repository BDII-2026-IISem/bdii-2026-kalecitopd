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
    from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Sale
from .serializers import SaleSerializer

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        sale = self.get_object()
        sale.is_paid = False  # O puedes cambiar un campo de estado si lo agregas
        sale.save()
        return Response({'status': 'venta anulada con éxito'}, status=status.HTTP_200_OK)