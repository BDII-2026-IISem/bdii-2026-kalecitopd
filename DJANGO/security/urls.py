from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RoleViewSet, RoleUserViewSet, ResourceViewSet, 
    ResourceRoleViewSet, CustomLoginView, LogoutView, ProfileView,
    CheckResourceAccessView
)

router = DefaultRouter()
router.register(r'roles', RoleViewSet)
router.register(r'role-users', RoleUserViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'resource-roles', ResourceRoleViewSet)

urlpatterns = [
    path('auth/login/', CustomLoginView.as_view(), name='custom_login'),
    path('auth/logout/', LogoutView.as_view(), name='custom_logout'),
    path('auth/profile/', ProfileView.as_view(), name='custom_profile'),
    path('auth/access/<str:resource_name>/', CheckResourceAccessView.as_view(), name='check_resource_access'),
    path('', include(router.urls)),
]