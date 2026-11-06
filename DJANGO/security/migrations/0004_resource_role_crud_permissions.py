from django.db import migrations, models


def preserve_existing_access(apps, schema_editor):
    ResourceRole = apps.get_model("security", "ResourceRole")
    ResourceRole.objects.using(schema_editor.connection.alias).update(
        can_create=True,
        can_read=True,
        can_update=True,
        can_delete=True,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("security", "0003_normalize_initial_role_names"),
    ]

    operations = [
        migrations.AddField(
            model_name="resourcerole",
            name="can_create",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="resourcerole",
            name="can_read",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="resourcerole",
            name="can_update",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="resourcerole",
            name="can_delete",
            field=models.BooleanField(default=False),
        ),
        migrations.RunPython(
            preserve_existing_access,
            reverse_code=migrations.RunPython.noop,
        ),
    ]
