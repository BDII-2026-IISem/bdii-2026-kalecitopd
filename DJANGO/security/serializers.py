from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Resource, ResourceRole, Role, RoleUser

User = get_user_model()

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class RoleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleUser
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class ResourceRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceRole
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "phone",
            "is_active",
            "password",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if not password:
            raise serializers.ValidationError(
                {"password": "La contraseña es obligatoria al crear un usuario."}
            )
        user = User(**validated_data)
        validate_password(password, user)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            validate_password(password, instance)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save(update_fields=("password",))
        return instance


class ProfileUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField()