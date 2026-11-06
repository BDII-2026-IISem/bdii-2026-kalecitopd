from django.db import migrations


ROLE_NAME_MAP = {
    "Administrador": "ADMIN",
    "Recepcionista": "RECEPCION",
    "Odontólogo": "ODONTOLOGO",
    "Auxiliar": "AUXILIAR",
    "Cartera": "CARTERA",
}


def normalize_initial_role_names(apps, schema_editor):
    Role = apps.get_model("security", "Role")
    RoleUser = apps.get_model("security", "RoleUser")
    ResourceRole = apps.get_model("security", "ResourceRole")
    database = schema_editor.connection.alias

    for old_name, new_name in ROLE_NAME_MAP.items():
        old_role = Role.objects.using(database).filter(name=old_name).first()
        if old_role is None:
            continue

        new_role = Role.objects.using(database).filter(name=new_name).first()
        if new_role is None:
            old_role.name = new_name
            old_role.save(using=database, update_fields=["name"])
            continue

        if not new_role.description and old_role.description:
            new_role.description = old_role.description
            new_role.save(using=database, update_fields=["description"])

        for assignment in RoleUser.objects.using(database).filter(role_id=old_role.pk):
            RoleUser.objects.using(database).get_or_create(
                user_id=assignment.user_id,
                role_id=new_role.pk,
            )
        for grant in ResourceRole.objects.using(database).filter(role_id=old_role.pk):
            ResourceRole.objects.using(database).get_or_create(
                role_id=new_role.pk,
                resource_id=grant.resource_id,
            )

        old_role.delete(using=database)


class Migration(migrations.Migration):
    dependencies = [
        ("security", "0002_alter_resource_options_alter_resourcerole_options_and_more"),
    ]

    operations = [
        migrations.RunPython(
            normalize_initial_role_names,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
