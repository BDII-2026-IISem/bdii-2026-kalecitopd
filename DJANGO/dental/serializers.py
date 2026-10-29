from django.db import transaction
from django.db.models import Sum
from rest_framework import serializers

from .models import (
    Appointment,
    Chair,
    ClinicalEvolution,
    ClinicalHistory,
    ClinicalSession,
    Odontologist,
    Payment,
    Procedure,
    SessionTreatment,
    TreatmentDetail,
    TreatmentPlan,
)


class OdontologistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odontologist
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class ChairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chair
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, attrs):
        instance = self.instance
        patient = attrs.get("patient", getattr(instance, "patient", None))
        odontologist = attrs.get(
            "odontologist", getattr(instance, "odontologist", None)
        )
        chair = attrs.get("chair", getattr(instance, "chair", None))
        start_time = attrs.get("start_time", getattr(instance, "start_time", None))
        end_time = attrs.get("end_time", getattr(instance, "end_time", None))
        status_value = attrs.get("status", getattr(instance, "status", None))

        if (
            instance
            and ClinicalSession.objects.filter(appointment=instance).exists()
            and any(
                attrs.get(field, getattr(instance, field)) != getattr(instance, field)
                for field in (
                    "patient",
                    "odontologist",
                    "chair",
                    "start_time",
                    "end_time",
                )
            )
        ):
            raise serializers.ValidationError(
                "No se puede reasignar una cita que ya tiene una sesión clínica."
            )
        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError(
                {"end_time": "La cita debe terminar después de iniciar."}
            )
        if status_value != Appointment.Status.CANCELLED:
            overlapping = Appointment.objects.filter(
                status__in=(Appointment.Status.SCHEDULED, Appointment.Status.CONFIRMED),
                start_time__lt=end_time,
                end_time__gt=start_time,
            )
            if instance:
                overlapping = overlapping.exclude(pk=instance.pk)
            conflicts = {}
            if overlapping.filter(odontologist=odontologist).exists():
                conflicts["odontologist"] = (
                    "El odontólogo ya tiene una cita en ese horario."
                )
            if overlapping.filter(chair=chair).exists():
                conflicts["chair"] = "El sillón ya está ocupado en ese horario."
            if overlapping.filter(patient=patient).exists():
                conflicts["patient"] = (
                    "El paciente ya tiene una cita en ese horario."
                )
            if conflicts:
                raise serializers.ValidationError(conflicts)
        return attrs


class ClinicalEvolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalEvolution
        fields = (
            "id",
            "clinical_history",
            "findings",
            "procedures",
            "materials_used",
            "consent_signed_at",
            "created_by",
            "created_at",
        )
        read_only_fields = ("id", "clinical_history", "created_by", "created_at")


class ClinicalHistorySerializer(serializers.ModelSerializer):
    evolutions = ClinicalEvolutionSerializer(many=True, read_only=True)

    class Meta:
        model = ClinicalHistory
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "evolutions")


class TreatmentPlanSerializer(serializers.ModelSerializer):
    total_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    paid_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    balance_due = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    details = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = TreatmentPlan
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class TreatmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentDetail
        fields = "__all__"
        read_only_fields = ("total", "created_at", "updated_at")

    def validate(self, attrs):
        quantity = attrs.get("quantity", getattr(self.instance, "quantity", 1))
        approved_quantity = attrs.get(
            "approved_quantity",
            getattr(self.instance, "approved_quantity", 0),
        )
        if approved_quantity > quantity:
            raise serializers.ValidationError(
                {"approved_quantity": "No puede superar la cantidad planeada."}
            )
        if self.instance:
            executed = self.instance.executed_sessions.aggregate(
                total=Sum("quantity")
            )["total"] or 0
            if approved_quantity < executed:
                raise serializers.ValidationError(
                    {
                        "approved_quantity": (
                            "No puede ser menor a la cantidad ya ejecutada."
                        )
                    }
                )
        return attrs


class SessionTreatmentInputSerializer(serializers.Serializer):
    treatment_detail = serializers.PrimaryKeyRelatedField(
        queryset=TreatmentDetail.objects.select_related("treatment_plan")
    )
    quantity = serializers.IntegerField(min_value=1)
    materials_used = serializers.CharField(required=False, allow_blank=True, default="")


class SessionTreatmentSerializer(serializers.ModelSerializer):
    procedure = serializers.CharField(
        source="treatment_detail.procedure.name",
        read_only=True,
    )

    class Meta:
        model = SessionTreatment
        fields = ("id", "treatment_detail", "procedure", "quantity", "materials_used")


class ClinicalSessionSerializer(serializers.ModelSerializer):
    treatment_details = SessionTreatmentInputSerializer(
        many=True,
        write_only=True,
        required=False,
    )
    executed_treatments = SessionTreatmentSerializer(many=True, read_only=True)

    class Meta:
        model = ClinicalSession
        fields = (
            "id",
            "appointment",
            "treatment_plan",
            "start_time",
            "end_time",
            "total",
            "status",
            "observations",
            "treatment_details",
            "executed_treatments",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "total", "created_at", "updated_at")

    def validate(self, attrs):
        instance = self.instance
        appointment = attrs.get(
            "appointment", getattr(instance, "appointment", None)
        )
        treatment_plan = attrs.get(
            "treatment_plan", getattr(instance, "treatment_plan", None)
        )
        start_time = attrs.get("start_time", getattr(instance, "start_time", None))
        end_time = attrs.get("end_time", getattr(instance, "end_time", None))

        if end_time and start_time and end_time <= start_time:
            raise serializers.ValidationError(
                {"end_time": "La sesión debe terminar después de iniciar."}
            )
        if (
            appointment
            and treatment_plan
            and appointment.patient_id != treatment_plan.patient_id
        ):
            raise serializers.ValidationError(
                {"treatment_plan": "El plan debe pertenecer al paciente de la cita."}
            )

        if (
            instance
            and instance.executed_treatments.exists()
            and (
                appointment.pk != instance.appointment_id
                or treatment_plan.pk != instance.treatment_plan_id
            )
        ):
            raise serializers.ValidationError(
                "No se puede reasignar una sesión con procedimientos ejecutados."
            )

        lines = attrs.get("treatment_details")
        if instance and lines is not None:
            raise serializers.ValidationError(
                {
                    "treatment_details": (
                        "Las ejecuciones registradas no se pueden reemplazar."
                    )
                }
            )
        if lines is not None and treatment_plan is not None:
            quantities = {}
            for line in lines:
                detail = line["treatment_detail"]
                quantity = line["quantity"]
                if detail.treatment_plan_id != treatment_plan.pk:
                    raise serializers.ValidationError(
                        {
                            "treatment_details": (
                                "Cada detalle debe pertenecer al plan de la sesión."
                            )
                        }
                    )
                quantities[detail.pk] = quantities.get(detail.pk, 0) + quantity
            if len(quantities) != len(lines):
                raise serializers.ValidationError(
                    {"treatment_details": "No repitas un detalle en la misma sesión."}
                )

            for detail_id, quantity in quantities.items():
                detail = TreatmentDetail.objects.get(pk=detail_id)
                previous = SessionTreatment.objects.filter(
                    treatment_detail=detail
                )
                if instance:
                    previous = previous.exclude(clinical_session=instance)
                already_executed = previous.aggregate(total=Sum("quantity"))["total"] or 0
                if detail.approved_quantity <= 0:
                    raise serializers.ValidationError(
                        {"treatment_details": "No se puede ejecutar un detalle sin aprobación."}
                    )
                if already_executed + quantity > detail.approved_quantity:
                    raise serializers.ValidationError(
                        {
                            "treatment_details": (
                                "La cantidad ejecutada supera la cantidad aprobada."
                            )
                        }
                    )
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        lines = validated_data.pop("treatment_details", [])
        session = ClinicalSession.objects.create(**validated_data)
        self._save_lines(session, lines)
        session.recalculate_total()
        return session

    @transaction.atomic
    def update(self, instance, validated_data):
        validated_data.pop("treatment_details", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        instance.full_clean()
        instance.save()
        instance.recalculate_total()
        return instance

    @staticmethod
    def _save_lines(session, lines):
        for line in lines:
            SessionTreatment.objects.create(
                clinical_session=session,
                **line,
            )


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

    def validate(self, attrs):
        instance = self.instance
        treatment_plan = attrs.get(
            "treatment_plan", getattr(instance, "treatment_plan", None)
        )
        amount = attrs.get("amount", getattr(instance, "amount", None))
        status_value = attrs.get("status", getattr(instance, "status", Payment.Status.PENDING))
        if (
            instance
            and instance.status == Payment.Status.CONFIRMED
            and status_value == Payment.Status.CONFIRMED
            and any(
                attrs.get(field, getattr(instance, field)) != getattr(instance, field)
                for field in ("amount", "treatment_plan", "method", "paid_at")
            )
        ):
            raise serializers.ValidationError(
                "Un pago confirmado no se puede modificar; cámbialo a cancelado."
            )
        if amount is not None and amount <= 0:
            raise serializers.ValidationError({"amount": "El monto debe ser mayor que cero."})
        if (
            treatment_plan
            and amount is not None
            and status_value == Payment.Status.CONFIRMED
        ):
            confirmed = treatment_plan.payments.filter(status=Payment.Status.CONFIRMED)
            if instance:
                confirmed = confirmed.exclude(pk=instance.pk)
            paid = confirmed.aggregate(total=Sum("amount"))["total"] or 0
            if paid + amount > treatment_plan.total_amount:
                raise serializers.ValidationError(
                    {"amount": "El pago supera el saldo pendiente del plan."}
                )
        return attrs
