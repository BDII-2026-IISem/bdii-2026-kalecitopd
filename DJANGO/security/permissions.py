from django.db import models
from rest_framework import permissions
from .models import RoleUser, ResourceRole


METHOD_PERMISSION = {
    "GET": "can_read",
    "HEAD": "can_read",
    "OPTIONS": "can_read",
    "POST": "can_create",
    "PUT": "can_update",
    "PATCH": "can_update",
    "DELETE": "can_delete",
}


def has_resource_access(user, resource_name):
    if user.is_superuser:
        return True
    user_roles = RoleUser.objects.filter(user=user).values_list('role', flat=True)
    return ResourceRole.objects.filter(
        role__in=user_roles, 
        resource__name=resource_name,
    ).filter(
        models.Q(can_create=True)
        | models.Q(can_read=True)
        | models.Q(can_update=True)
        | models.Q(can_delete=True)
    ).exists()


def has_resource_permission(user, resource_name, method):
    if user.is_superuser:
        return True
    permission_field = METHOD_PERMISSION.get(method.upper())
    if permission_field is None:
        return False
    user_roles = RoleUser.objects.filter(user=user).values_list('role', flat=True)
    return ResourceRole.objects.filter(
        role__in=user_roles,
        resource__name=resource_name,
        **{permission_field: True},
    ).exists()


class HasResourcePermission(permissions.BasePermission):
    """
    Permiso que valida si el usuario tiene acceso al recurso definido en la vista.
    La vista debe tener el atributo `resource_name`.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Si la vista define un resource_name, lo validamos
        resource_name = getattr(view, 'resource_name', None)
        if not resource_name:
            return True # Si no requiere recurso específico, permite según autenticación
        
        return has_resource_permission(request.user, resource_name, request.method)