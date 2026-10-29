import decimal

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("client", "0003_patient"),
    ]

    operations = [
        migrations.CreateModel(
            name="Chair",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("name", models.CharField(max_length=100, unique=True, verbose_name="Nombre")),
                ("description", models.TextField(blank=True, verbose_name="Descripción")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
            ],
            options={
                "verbose_name": "Sillón",
                "verbose_name_plural": "Sillones",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Odontologist",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("name", models.CharField(max_length=150, verbose_name="Nombre")),
                ("description", models.TextField(blank=True, verbose_name="Descripción")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
            ],
            options={
                "verbose_name": "Odontólogo",
                "verbose_name_plural": "Odontólogos",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Procedure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("name", models.CharField(max_length=150, verbose_name="Nombre")),
                ("description", models.TextField(blank=True, verbose_name="Descripción")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activo")),
            ],
            options={
                "verbose_name": "Procedimiento",
                "verbose_name_plural": "Procedimientos",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="TreatmentPlan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("name", models.CharField(max_length=150, verbose_name="Nombre")),
                ("description", models.TextField(blank=True, verbose_name="Descripción")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Borrador"),
                            ("active", "Activo"),
                            ("completed", "Completado"),
                            ("cancelled", "Cancelado"),
                        ],
                        default="draft",
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="treatment_plans",
                        to="client.patient",
                        verbose_name="Paciente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Plan de tratamiento",
                "verbose_name_plural": "Planes de tratamiento",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="Appointment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("start_time", models.DateTimeField(verbose_name="Fecha y hora de inicio")),
                ("end_time", models.DateTimeField(verbose_name="Fecha y hora de finalización")),
                ("motive", models.CharField(max_length=255, verbose_name="Motivo")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("scheduled", "Programada"),
                            ("confirmed", "Confirmada"),
                            ("completed", "Completada"),
                            ("cancelled", "Cancelada"),
                            ("no_show", "No asistió"),
                        ],
                        default="scheduled",
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                (
                    "chair",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="appointments",
                        to="dental.chair",
                        verbose_name="Sillón",
                    ),
                ),
                (
                    "odontologist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="appointments",
                        to="dental.odontologist",
                        verbose_name="Odontólogo",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="appointments",
                        to="client.patient",
                        verbose_name="Paciente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Cita",
                "verbose_name_plural": "Citas",
                "ordering": ("-start_time",),
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(end_time__gt=models.F("start_time")),
                        name="appointment_end_after_start",
                    )
                ],
            },
        ),
        migrations.CreateModel(
            name="ClinicalHistory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                (
                    "name",
                    models.CharField(
                        default="Historia clínica",
                        max_length=150,
                        verbose_name="Nombre",
                    ),
                ),
                ("description", models.TextField(blank=True, verbose_name="Descripción")),
                ("is_active", models.BooleanField(default=True, verbose_name="Activa")),
                (
                    "patient",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="clinical_history",
                        to="client.patient",
                        verbose_name="Paciente",
                    ),
                ),
            ],
            options={
                "verbose_name": "Historia clínica",
                "verbose_name_plural": "Historias clínicas",
            },
        ),
        migrations.CreateModel(
            name="ClinicalEvolution",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("findings", models.TextField(verbose_name="Hallazgos")),
                ("procedures", models.TextField(blank=True, verbose_name="Procedimientos realizados")),
                ("materials_used", models.TextField(blank=True, verbose_name="Materiales utilizados")),
                (
                    "consent_signed_at",
                    models.DateTimeField(
                        blank=True,
                        null=True,
                        verbose_name="Fecha de consentimiento",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="clinical_evolutions",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Registrado por",
                    ),
                ),
                (
                    "clinical_history",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="evolutions",
                        to="dental.clinicalhistory",
                        verbose_name="Historia clínica",
                    ),
                ),
            ],
            options={
                "verbose_name": "Evolución clínica",
                "verbose_name_plural": "Evoluciones clínicas",
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="TreatmentDetail",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("quantity", models.PositiveIntegerField(default=1, verbose_name="Cantidad")),
                ("approved_quantity", models.PositiveIntegerField(default=0, verbose_name="Cantidad aprobada")),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Valor unitario")),
                ("total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, verbose_name="Total")),
                ("observations", models.TextField(blank=True, verbose_name="Observaciones")),
                (
                    "procedure",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="treatment_details",
                        to="dental.procedure",
                        verbose_name="Procedimiento",
                    ),
                ),
                (
                    "treatment_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="details",
                        to="dental.treatmentplan",
                        verbose_name="Plan de tratamiento",
                    ),
                ),
            ],
            options={
                "verbose_name": "Detalle de tratamiento",
                "verbose_name_plural": "Detalles de tratamiento",
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(quantity__gt=0),
                        name="treatment_qty_positive",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(approved_quantity__lte=models.F("quantity")),
                        name="treatment_approved_lte_qty",
                    ),
                    models.CheckConstraint(
                        condition=models.Q(unit_price__gte=0),
                        name="treatment_price_nonnegative",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="ClinicalSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")),
                ("start_time", models.DateTimeField(verbose_name="Fecha y hora de inicio")),
                ("end_time", models.DateTimeField(blank=True, null=True, verbose_name="Fecha y hora de finalización")),
                ("total", models.DecimalField(decimal_places=2, default=decimal.Decimal("0.00"), max_digits=12, verbose_name="Total ejecutado")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("scheduled", "Programada"),
                            ("in_progress", "En curso"),
                            ("completed", "Completada"),
                            ("cancelled", "Cancelada"),
                        ],
                        default="scheduled",
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                ("observations", models.TextField(blank=True, verbose_name="Observaciones")),
                (
                    "appointment",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="clinical_session",
                        to="dental.appointment",
                        verbose_name="Cita",
                    ),
                ),
                (
                    "treatment_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="sessions",
                        to="dental.treatmentplan",
                        verbose_name="Plan de tratamiento",
                    ),
                ),
            ],
            options={
                "verbose_name": "Sesión clínica",
                "verbose_name_plural": "Sesiones clínicas",
                "ordering": ("-start_time",),
            },
        ),
        migrations.CreateModel(
            name="SessionTreatment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(default=1, verbose_name="Cantidad ejecutada")),
                ("materials_used", models.TextField(blank=True, verbose_name="Materiales utilizados")),
                (
                    "clinical_session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="executed_treatments",
                        to="dental.clinicalsession",
                        verbose_name="Sesión clínica",
                    ),
                ),
                (
                    "treatment_detail",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="executed_sessions",
                        to="dental.treatmentdetail",
                        verbose_name="Detalle de tratamiento aprobado",
                    ),
                ),
            ],
            options={
                "verbose_name": "Procedimiento ejecutado en sesión",
                "verbose_name_plural": "Procedimientos ejecutados en sesión",
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(quantity__gt=0),
                        name="session_qty_positive",
                    ),
                    models.UniqueConstraint(
                        fields=("clinical_session", "treatment_detail"),
                        name="session_detail_unique",
                    ),
                ],
            },
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "method",
                    models.CharField(
                        choices=[
                            ("cash", "Efectivo"),
                            ("card", "Tarjeta"),
                            ("transfer", "Transferencia"),
                            ("other", "Otro"),
                        ],
                        max_length=20,
                        verbose_name="Método de pago",
                    ),
                ),
                ("amount", models.DecimalField(decimal_places=2, max_digits=12, verbose_name="Monto")),
                ("paid_at", models.DateTimeField(verbose_name="Fecha de pago")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pendiente"),
                            ("confirmed", "Confirmado"),
                            ("cancelled", "Cancelado"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Estado",
                    ),
                ),
                (
                    "treatment_plan",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="payments",
                        to="dental.treatmentplan",
                        verbose_name="Plan de tratamiento",
                    ),
                ),
            ],
            options={
                "verbose_name": "Pago",
                "verbose_name_plural": "Pagos",
                "ordering": ("-paid_at",),
                "constraints": [
                    models.CheckConstraint(
                        condition=models.Q(amount__gt=0),
                        name="payment_amount_positive",
                    )
                ],
            },
        ),
    ]
