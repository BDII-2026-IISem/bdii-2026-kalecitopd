from django.core.management.base import BaseCommand
from security.models import Role, Resource, ResourceRole

class Command(BaseCommand):
    help = 'Semilla inicial para poblar roles y recursos del sistema RBAC de OdontoNova'

    def handle(self, *args, **kwargs):
        self.stdout.write("Iniciando siembra de datos de seguridad...")

        role_resources = {
            "Administrador": (
                "pacientes",
                "odontologos",
                "sillones",
                "citas",
                "historias",
                "tratamientos",
                "procedimientos",
                "detalles-tratamiento",
                "sesiones",
                "pagos",
                "roles",
                "role-users",
                "resources",
                "resource-roles",
                "users",
            ),
            "Recepcionista": (
                "pacientes",
                "odontologos",
                "sillones",
                "citas",
            ),
            "Odontólogo": (
                "pacientes",
                "citas",
                "historias",
                "tratamientos",
                "procedimientos",
                "detalles-tratamiento",
                "sesiones",
            ),
            "Auxiliar": (
                "pacientes",
                "citas",
                "historias",
                "procedimientos",
                "sesiones",
            ),
            "Cartera": (
                "pacientes",
                "tratamientos",
                "pagos",
            ),
        }

        # 1. Crear los roles iniciales sin eliminar los existentes.
        role_objs = {}
        for role_name in role_resources:
            role, created = Role.objects.get_or_create(name=role_name)
            role_objs[role_name] = role
            if created:
                self.stdout.write(self.style.SUCCESS(f"Rol creado: {role_name}"))

        # 2. Crear los recursos del dominio odontológico y seguridad.
        resources = {
            resource_name
            for role_resource_names in role_resources.values()
            for resource_name in role_resource_names
        }
        resource_objs = {}
        for res_name in sorted(resources):
            resource, created = Resource.objects.get_or_create(name=res_name)
            resource_objs[res_name] = resource
            if created:
                self.stdout.write(self.style.SUCCESS(f"Recurso creado: {res_name}"))

        # 3. Sincronizar los permisos sin retirar asignaciones manuales previas.
        for role_name, resource_names in role_resources.items():
            role = role_objs[role_name]
            for resource_name in resource_names:
                _, created = ResourceRole.objects.get_or_create(
                    role=role,
                    resource=resource_objs[resource_name],
                )
                if created:
                    self.stdout.write(
                        f"Permiso asignado: {role_name} -> {resource_name}"
                    )

        self.stdout.write(self.style.SUCCESS("¡Siembra de seguridad completada con éxito!"))