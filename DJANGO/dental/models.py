from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum

from client.models import Patient


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        abstract = True


class Odontologist(TimestampedModel):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Odontólogo"
        verbose_name_plural = "Odontólogos"
        ordering = ("name",)


class Chair(TimestampedModel):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sillón"
        verbose_name_plural = "Sillones"
        ordering = ("name",)


class Appointment(TimestampedModel):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Programada"
        CONFIRMED = "confirmed", "Confirmada"
        COMPLETED = "completed", "Completada"
        CANCELLED = "cancelled", "Cancelada"
        NO_SHOW = "no_show", "No asistió"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Paciente",
    )
    odontologist = models.ForeignKey(
        Odontologist,
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Odontólogo",
    )
    chair = models.ForeignKey(
        Chair,
        on_delete=models.PROTECT,
        related_name="appointments",
        verbose_name="Sillón",
    )
    start_time = models.DateTimeField(verbose_name="Fecha y hora de inicio")
    end_time = models.DateTimeField(verbose_name="Fecha y hora de finalización")
    motive = models.CharField(max_length=255, verbose_name="Motivo")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name="Estado",
    )

    def clean(self):
        super().clean()
        if self.start_time and self.end_time and self.end_time <= self.start_time:
            raise ValidationError({"end_time": "La cita debe terminar después de iniciar."})
        if self.pk and ClinicalSession.objects.filter(appointment_id=self.pk).exists():
            original = Appointment.objects.get(pk=self.pk)
            if any(
                getattr(self, field) != getattr(original, field)
                for field in (
                    "patient_id",
                    "odontologist_id",
                    "chair_id",
                    "start_time",
                    "end_time",
                )
            ):
                raise ValidationError(
                    "No se puede reasignar una cita que ya tiene una sesión clínica."
                )
        if (
            self.status != self.Status.CANCELLED
            and self.start_time
            and self.end_time
            and self.odontologist_id
            and self.chair_id
        ):
            conflicts = Appointment.objects.filter(
                status__in=(self.Status.SCHEDULED, self.Status.CONFIRMED),
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            )
            if self.pk:
                conflicts = conflicts.exclude(pk=self.pk)
            if conflicts.filter(odontologist_id=self.odontologist_id).exists():
                raise ValidationError(
                    {"odontologist": "El odontólogo ya tiene una cita en ese horario."}
                )
            if conflicts.filter(chair_id=self.chair_id).exists():
                raise ValidationError({"chair": "El sillón ya está ocupado en ese horario."})
            if conflicts.filter(patient_id=self.patient_id).exists():
                raise ValidationError({"patient": "El paciente ya tiene una cita en ese horario."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient} - {self.start_time:%Y-%m-%d %H:%M}"

    class Meta:
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ("-start_time",)
        constraints = [
            models.CheckConstraint(
                condition=models.Q(end_time__gt=models.F("start_time")),
                name="appointment_end_after_start",
            )
        ]


class ClinicalHistory(TimestampedModel):
    patient = models.OneToOneField(
        Patient,
        on_delete=models.PROTECT,
        related_name="clinical_history",
        verbose_name="Paciente",
    )
    name = models.CharField(
        max_length=150,
        default="Historia clínica",
        verbose_name="Nombre",
    )
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activa")

    def __str__(self):
        return f"{self.name} - {self.patient}"

    class Meta:
        verbose_name = "Historia clínica"
        verbose_name_plural = "Historias clínicas"


class TreatmentPlan(TimestampedModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        ACTIVE = "active", "Activo"
        COMPLETED = "completed", "Completado"
        CANCELLED = "cancelled", "Cancelado"

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name="treatment_plans",
        verbose_name="Paciente",
    )
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name="Estado",
    )

    @property
    def total_amount(self):
        amount = self.details.aggregate(total=Sum("total"))["total"]
        return amount if amount is not None else Decimal("0.00")

    @property
    def paid_amount(self):
        amount = self.payments.filter(status=Payment.Status.CONFIRMED).aggregate(
            total=Sum("amount")
        )["total"]
        return amount if amount is not None else Decimal("0.00")

    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"{self.name} - {self.patient}"

    class Meta:
        verbose_name = "Plan de tratamiento"
        verbose_name_plural = "Planes de tratamiento"
        ordering = ("-created_at",)


class Procedure(TimestampedModel):
    name = models.CharField(max_length=150, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Procedimiento"
        verbose_name_plural = "Procedimientos"
        ordering = ("name",)


class TreatmentDetail(TimestampedModel):
    treatment_plan = models.ForeignKey(
        TreatmentPlan,
        on_delete=models.PROTECT,
        related_name="details",
        verbose_name="Plan de tratamiento",
    )
    procedure = models.ForeignKey(
        Procedure,
        on_delete=models.PROTECT,
        related_name="treatment_details",
        verbose_name="Procedimiento",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    approved_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Cantidad aprobada",
    )
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Valor unitario",
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Total",
    )
    observations = models.TextField(blank=True, verbose_name="Observaciones")

    def clean(self):
        super().clean()
        if self.approved_quantity > self.quantity:
            raise ValidationError(
                {"approved_quantity": "La cantidad aprobada no puede superar la cantidad planeada."}
            )
        already_executed = 0
        if self.pk:
            already_executed = self.executed_sessions.aggregate(
                total=Sum("quantity")
            )["total"] or 0
        if self.approved_quantity < already_executed:
            raise ValidationError(
                {"approved_quantity": "No puede ser menor a la cantidad ya ejecutada."}
            )

    def save(self, *args, **kwargs):
        if self.unit_price is not None:
            self.total = self.unit_price * self.quantity
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.procedure} ({self.treatment_plan})"

    class Meta:
        verbose_name = "Detalle de tratamiento"
        verbose_name_plural = "Detalles de tratamiento"
        constraints = [
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
        ]


class ClinicalSession(TimestampedModel):
    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Programada"
        IN_PROGRESS = "in_progress", "En curso"
        COMPLETED = "completed", "Completada"
        CANCELLED = "cancelled", "Cancelada"

    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.PROTECT,
        related_name="clinical_session",
        verbose_name="Cita",
    )
    treatment_plan = models.ForeignKey(
        TreatmentPlan,
        on_delete=models.PROTECT,
        related_name="sessions",
        verbose_name="Plan de tratamiento",
    )
    start_time = models.DateTimeField(verbose_name="Fecha y hora de inicio")
    end_time = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha y hora de finalización",
    )
    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Total ejecutado",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name="Estado",
    )
    observations = models.TextField(blank=True, verbose_name="Observaciones")

    def clean(self):
        super().clean()
        if self.end_time and self.start_time and self.end_time <= self.start_time:
            raise ValidationError({"end_time": "La sesión debe terminar después de iniciar."})
        if (
            self.appointment_id
            and self.treatment_plan_id
            and self.appointment.patient_id != self.treatment_plan.patient_id
        ):
            raise ValidationError(
                {"treatment_plan": "El plan debe pertenecer al paciente de la cita."}
            )
        if self.pk and self.executed_treatments.exists():
            original = ClinicalSession.objects.get(pk=self.pk)
            if (
                self.appointment_id != original.appointment_id
                or self.treatment_plan_id != original.treatment_plan_id
            ):
                raise ValidationError(
                    "No se puede reasignar una sesión con procedimientos ejecutados."
                )

    def recalculate_total(self):
        value = sum(
            (
                line.quantity * line.treatment_detail.unit_price
                for line in self.executed_treatments.select_related("treatment_detail")
            ),
            Decimal("0.00"),
        )
        type(self).objects.filter(pk=self.pk).update(total=value)
        self.total = value

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sesión de {self.appointment}"

    class Meta:
        verbose_name = "Sesión clínica"
        verbose_name_plural = "Sesiones clínicas"
        ordering = ("-start_time",)


class SessionTreatment(models.Model):
    clinical_session = models.ForeignKey(
        ClinicalSession,
        on_delete=models.PROTECT,
        related_name="executed_treatments",
        verbose_name="Sesión clínica",
    )
    treatment_detail = models.ForeignKey(
        TreatmentDetail,
        on_delete=models.PROTECT,
        related_name="executed_sessions",
        verbose_name="Detalle de tratamiento aprobado",
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad ejecutada")
    materials_used = models.TextField(blank=True, verbose_name="Materiales utilizados")

    def save(self, *args, **kwargs):
        self.full_clean()
        result = super().save(*args, **kwargs)
        self.clinical_session.recalculate_total()
        return result

    def delete(self, *args, **kwargs):
        session = self.clinical_session
        result = super().delete(*args, **kwargs)
        session.recalculate_total()
        return result

    def clean(self):
        super().clean()
        if (
            self.clinical_session_id
            and self.treatment_detail_id
            and self.clinical_session.treatment_plan_id
            != self.treatment_detail.treatment_plan_id
        ):
            raise ValidationError(
                {"treatment_detail": "El detalle debe pertenecer al plan de la sesión."}
            )
        if self.clinical_session_id and self.treatment_detail_id:
            already_executed = self.treatment_detail.executed_sessions.exclude(
                pk=self.pk
            ).aggregate(total=Sum("quantity"))["total"] or 0
            if (
                self.treatment_detail.approved_quantity <= 0
                or already_executed + self.quantity
                > self.treatment_detail.approved_quantity
            ):
                raise ValidationError(
                    {"quantity": "La cantidad ejecutada supera la cantidad aprobada."}
                )

    def __str__(self):
        return f"{self.treatment_detail} - {self.quantity}"

    class Meta:
        verbose_name = "Procedimiento ejecutado en sesión"
        verbose_name_plural = "Procedimientos ejecutados en sesión"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="session_qty_positive",
            ),
            models.UniqueConstraint(
                fields=("clinical_session", "treatment_detail"),
                name="session_detail_unique",
            )
        ]


class ClinicalEvolution(models.Model):
    clinical_history = models.ForeignKey(
        ClinicalHistory,
        on_delete=models.PROTECT,
        related_name="evolutions",
        verbose_name="Historia clínica",
    )
    findings = models.TextField(verbose_name="Hallazgos")
    procedures = models.TextField(blank=True, verbose_name="Procedimientos realizados")
    materials_used = models.TextField(blank=True, verbose_name="Materiales utilizados")
    consent_signed_at = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name="Fecha de consentimiento",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="clinical_evolutions",
        verbose_name="Registrado por",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de registro")

    def __str__(self):
        return f"Evolución de {self.clinical_history.patient} ({self.created_at:%Y-%m-%d})"

    class Meta:
        verbose_name = "Evolución clínica"
        verbose_name_plural = "Evoluciones clínicas"
        ordering = ("-created_at",)


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = "cash", "Efectivo"
        CARD = "card", "Tarjeta"
        TRANSFER = "transfer", "Transferencia"
        OTHER = "other", "Otro"

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        CONFIRMED = "confirmed", "Confirmado"
        CANCELLED = "cancelled", "Cancelado"

    treatment_plan = models.ForeignKey(
        TreatmentPlan,
        on_delete=models.PROTECT,
        related_name="payments",
        verbose_name="Plan de tratamiento",
    )
    method = models.CharField(
        max_length=20,
        choices=Method.choices,
        verbose_name="Método de pago",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Monto",
    )
    paid_at = models.DateTimeField(verbose_name="Fecha de pago")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Estado",
    )

    def clean(self):
        super().clean()
        if self.amount is not None and self.amount <= 0:
            raise ValidationError({"amount": "El monto del pago debe ser mayor que cero."})
        if self.pk:
            original = Payment.objects.get(pk=self.pk)
            if original.status == self.Status.CONFIRMED and self.status == self.Status.CONFIRMED:
                immutable_fields = ("amount", "treatment_plan_id", "method", "paid_at")
                if any(
                    getattr(self, field) != getattr(original, field)
                    for field in immutable_fields
                ):
                    raise ValidationError(
                        "Un pago confirmado no se puede modificar; cámbialo a cancelado."
                    )
        if self.treatment_plan_id and self.status == self.Status.CONFIRMED:
            other_confirmed = self.treatment_plan.payments.filter(
                status=self.Status.CONFIRMED
            )
            if self.pk:
                other_confirmed = other_confirmed.exclude(pk=self.pk)
            already_paid = other_confirmed.aggregate(total=Sum("amount"))["total"]
            total = self.treatment_plan.total_amount
            if (already_paid or Decimal("0.00")) + self.amount > total:
                raise ValidationError(
                    {"amount": "El pago supera el saldo pendiente del plan."}
                )

    def __str__(self):
        return f"Pago {self.amount} - {self.treatment_plan}"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Pago"
        verbose_name_plural = "Pagos"
        ordering = ("-paid_at",)
        constraints = [
            models.CheckConstraint(
                condition=models.Q(amount__gt=0),
                name="payment_amount_positive",
            )
        ]
