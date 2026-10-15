from rest_framework import permissions
from .models import RoleUser, ResourceRole

def has_resource_access(user, resource_name):
    if user.is_superuser:
        return True
    user_roles = RoleUser.objects.filter(user=user).values_list('role', flat=True)
    return ResourceRole.objects.filter(
        role__in=user_roles, 
        resource__name=resource_name
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
        
        return has_resource_access(request.user, resource_name)