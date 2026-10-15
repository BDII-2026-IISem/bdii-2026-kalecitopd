from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    # Panel de administración de Django
    path('admin/', admin.site.urls),
    
    # Rutas de las aplicaciones de negocio y seguridad
    path('api/', include('client.urls')),
    path('api/', include('product.urls')),
    path('api/', include('sale.urls')),
    path('api/', include('security.urls')),
    
    # Autenticación web de DRF y JWT SimpleJWT
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Documentación de la API (drf-spectacular / Swagger)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]