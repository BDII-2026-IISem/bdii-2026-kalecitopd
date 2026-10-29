from django.contrib import admin

from .models import Resource, ResourceRole, Role, RoleUser


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(RoleUser)
class RoleUserAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "user__first_name", "user__last_name")
    autocomplete_fields = ("user", "role")


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(ResourceRole)
class ResourceRoleAdmin(admin.ModelAdmin):
    list_display = ("role", "resource")
    list_filter = ("role",)
    search_fields = ("role__name", "resource__name")
    autocomplete_fields = ("role", "resource")
