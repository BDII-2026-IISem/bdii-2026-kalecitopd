from django.shortcuts import render
from rest_framework import viewsets, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Role, RoleUser, Resource, ResourceRole
from .serializers import (
    RoleSerializer, RoleUserSerializer, 
    ResourceSerializer, ResourceRoleSerializer
)

# --- ViewSets de Seguridad ---
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleUserViewSet(viewsets.ModelViewSet):
    queryset = RoleUser.objects.all()
    serializer_class = RoleUserSerializer

class ResourceViewSet(viewsets.ModelViewSet):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer

class ResourceRoleViewSet(viewsets.ModelViewSet):
    queryset = ResourceRole.objects.all()
    serializer_class = ResourceRoleSerializer


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

            return Response({"detail": "Cierre de sesión exitoso."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
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
        }
        return Response(data, status=status.HTTP_200_OK)
    
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