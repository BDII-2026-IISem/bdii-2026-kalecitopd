from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SaleViewSet, SaleDetailViewSet

router = DefaultRouter()
router.register(r'sales', SaleViewSet)
router.register(r'sale-details', SaleDetailViewSet)

urlpatterns = [
    path('', include(router.urls)),
]