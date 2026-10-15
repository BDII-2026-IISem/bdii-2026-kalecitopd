from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('client.urls')),
    path('api/', include('product.urls')),
    path('api/', include('sale.urls')),
    path('api-auth/', include('rest_framework.urls')),  # Para login/logout en DRF
]