from django.contrib.auth import get_user_model
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.views import TokenRefreshView

from .permissions import HasResourcePermission
from .models import Role, RoleUser, Resource, ResourceRole
from .serializers import (
    RoleSerializer, RoleUserSerializer, 
    ResourceSerializer, ResourceRoleSerializer, UserSerializer,
    ProfileUpdateSerializer,
)

User = get_user_model()

# --- ViewSets de Seguridad ---
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = (permissions.IsAuthenticated, HasResourcePermission)
    resource_name = "roles"

class RoleUserViewSet(viewsets.ModelViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleUserSerializer
    permission_classes = (permissions.IsAuthenticated, HasResourcePermission)
    resource_name = "role-users"

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (permissions.IsAuthenticated, HasResourcePermission)
    resource_name = "resources"

class ResourceRoleViewSet(viewsets.ModelViewSet):
    queryset = ResourceRole.objects.all()
    serializer_class = ResourceRoleSerializer
    permission_classes = (permissions.IsAuthenticated, HasResourcePermission)
    resource_name = "resource-roles"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("username")
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, HasResourcePermission)
    resource_name = "users"


# --- Login Personalizado ---
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'is_superuser': self.user.is_superuser,
        }
        return data

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# --- Logout ---
class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"detail": "Se requiere el refresh token."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except TokenError:
            return Response(
                {"detail": "El refresh token no es válido o ya fue revocado."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class ProfileView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_superuser': user.is_superuser,
        }
        return Response(data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = ProfileUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.email = serializer.validated_data["email"]
        request.user.save(update_fields=("email",))
        return self.get(request)
    
def has_resource_access(user, resource_name):
    if user.is_superuser:
        return True
    user_roles = RoleUser.objects.filter(user=user).values_list('role', flat=True)
    has_access = ResourceRole.objects.filter(
        role__in=user_roles, 
        resource__name=resource_name
    ).exists()
    return has_access

class CheckResourceAccessView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, resource_name):
        allowed = has_resource_access(request.user, resource_name)
        return Response({
            "resource": resource_name,
            "has_access": allowed
        }, status=status.HTTP_200_OK)


class PermissionsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        if request.user.is_superuser:
            return Response({
                "permissions": [{
                    "resource": "*",
                    "method": "*",
                    "path": "/api/",
                    "roleId": None,
                    "roleName": "Superusuario",
                }]
            })

        role_ids = RoleUser.objects.filter(user=request.user).values_list(
            "role_id", flat=True
        )
        grants = ResourceRole.objects.filter(
            role_id__in=role_ids
        ).select_related("role", "resource").order_by("resource__name", "role__name")
        return Response({
            "permissions": [
                {
                    "resource": grant.resource.name,
                    "method": "*",
                    "path": f"/api/{grant.resource.name}/",
                    "roleId": grant.role_id,
                    "roleName": grant.role.name,
                }
                for grant in grants
            ]
        })