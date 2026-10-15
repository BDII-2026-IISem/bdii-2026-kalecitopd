from django.core.management.base import BaseCommand
from security.models import Role, Resource, ResourceRole

class Command(BaseCommand):
    help = 'Semilla inicial para poblar roles y recursos del sistema RBAC de OdontoNova'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando siembra de datos de seguridad...")

        # 1. Crear Roles por defecto
        roles = ['Administrador', 'Odontólogo', 'Recepcionista']
        role_objs = {}
        for role_name in roles:
            role, created = Role.objects.get_or_create(name=role_name)
            role_objs[role_name] = role
            if created:
                self.stdout.write(self.style.SUCCESS(f"Rol creado: {role_name}"))

        # 2. Crear Recursos de negocio por defecto
        resources = ['clients', 'products', 'sales', 'roles', 'resources']
        resource_objs = {}
        for res_name in resources:
            resource, created = Resource.objects.get_or_create(name=res_name)
            resource_objs[res_name] = resource
            if created:
                self.stdout.write(self.style.SUCCESS(f"Recurso creado: {res_name}"))

        # 3. Asignar todos los recursos al Administrador por defecto
        admin_role = role_objs['Administrador']
        for res_obj in resource_objs.values():
            _, created = ResourceRole.objects.get_or_create(role=admin_role, resource=res_obj)
            if created:
                self.stdout.write(f"Permiso asignado: Administrador -> {res_obj.name}")

        self.stdout.write(self.style.SUCCESS("¡Siembra de seguridad completada con éxito!"))