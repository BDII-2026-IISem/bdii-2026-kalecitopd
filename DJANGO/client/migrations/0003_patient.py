import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("client", "0002_client"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Client",
            new_name="Patient",
        ),
        migrations.AlterModelOptions(
            name="patient",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Paciente",
                "verbose_name_plural": "Pacientes",
            },
        ),
        migrations.AlterModelTable(
            name="patient",
            table="client_client",
        ),
        migrations.AddField(
            model_name="patient",
            name="document_type",
            field=models.CharField(
                default="legacy",
                max_length=30,
                verbose_name="Tipo de documento",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="patient",
            name="document_number",
            field=models.CharField(
                blank=True,
                max_length=30,
                null=True,
                unique=True,
                verbose_name="Número de documento",
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="date_of_birth",
            field=models.DateField(
                blank=True,
                null=True,
                verbose_name="Fecha de nacimiento",
            ),
        ),
        migrations.AddField(
            model_name="patient",
            name="updated_at",
            field=models.DateTimeField(
                default=django.utils.timezone.now,
                verbose_name="Fecha de actualización",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="patient",
            name="updated_at",
            field=models.DateTimeField(
                auto_now=True,
                verbose_name="Fecha de actualización",
            ),
        ),
    ]
