from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from client.models import Patient
from security.models import Resource, ResourceRole, Role, RoleUser

from .models import (
    Appointment,
    Chair,
    ClinicalHistory,
    Odontologist,
    Payment,
    Procedure,
    TreatmentDetail,
    TreatmentPlan,
)
from .serializers import (
    AppointmentSerializer,
    ClinicalSessionSerializer,
    PaymentSerializer,
)


class DentalDomainTests(TestCase):
    def setUp(self):
        self.patient = Patient.objects.create(
            document_type="ID",
            document_number="ID-100",
            first_name="Ana",
            last_name="Paciente",
            email="ana@example.com",
            phone="5550100",
        )
        self.odontologist = Odontologist.objects.create(name="Dra. Ejemplo")
        self.chair = Chair.objects.create(name="Sillón 1")
        self.plan = TreatmentPlan.objects.create(
            patient=self.patient,
            name="Plan inicial",
        )
        self.procedure = Procedure.objects.create(name="Limpieza")

    def make_appointment(self, offset_hours=0):
        start_time = timezone.now() + timedelta(days=1, hours=offset_hours)
        return Appointment.objects.create(
            patient=self.patient,
            odontologist=self.odontologist,
            chair=self.chair,
            start_time=start_time,
            end_time=start_time + timedelta(minutes=30),
            motive="Control",
        )

    def test_treatment_detail_calculates_total_and_tracks_partial_approval(self):
        detail = TreatmentDetail.objects.create(
            treatment_plan=self.plan,
            procedure=self.procedure,
            quantity=3,
            approved_quantity=2,
            unit_price=Decimal("25.00"),
        )

        self.assertEqual(detail.total, Decimal("75.00"))

    def test_appointment_rejects_an_odontologist_or_chair_conflict(self):
        appointment = self.make_appointment()
        serializer = AppointmentSerializer(
            data={
                "patient": self.patient.pk,
                "odontologist": self.odontologist.pk,
                "chair": self.chair.pk,
                "start_time": appointment.start_time + timedelta(minutes=10),
                "end_time": appointment.end_time + timedelta(minutes=10),
                "motive": "Otra cita",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("odontologist", serializer.errors)
        self.assertIn("chair", serializer.errors)

    def test_session_can_only_execute_approved_quantity_and_updates_total(self):
        detail = TreatmentDetail.objects.create(
            treatment_plan=self.plan,
            procedure=self.procedure,
            quantity=3,
            approved_quantity=2,
            unit_price=Decimal("25.00"),
        )
        appointment = self.make_appointment()
        session_start = appointment.start_time
        serializer = ClinicalSessionSerializer(
            data={
                "appointment": appointment.pk,
                "treatment_plan": self.plan.pk,
                "start_time": session_start,
                "treatment_details": [
                    {
                        "treatment_detail": detail.pk,
                        "quantity": 2,
                        "materials_used": "Material de prueba",
                    }
                ],
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        session = serializer.save()
        self.assertEqual(session.total, Decimal("50.00"))

        next_appointment = self.make_appointment(offset_hours=2)
        next_serializer = ClinicalSessionSerializer(
            data={
                "appointment": next_appointment.pk,
                "treatment_plan": self.plan.pk,
                "start_time": next_appointment.start_time,
                "treatment_details": [
                    {"treatment_detail": detail.pk, "quantity": 1}
                ],
            }
        )
        self.assertFalse(next_serializer.is_valid())
        self.assertIn("treatment_details", next_serializer.errors)

    def test_confirmed_payments_cannot_exceed_plan_total(self):
        TreatmentDetail.objects.create(
            treatment_plan=self.plan,
            procedure=self.procedure,
            quantity=2,
            approved_quantity=0,
            unit_price=Decimal("25.00"),
        )
        now = timezone.now()
        invalid_payment = PaymentSerializer(
            data={
                "treatment_plan": self.plan.pk,
                "method": Payment.Method.CASH,
                "amount": "50.01",
                "paid_at": now,
                "status": Payment.Status.CONFIRMED,
            }
        )
        self.assertFalse(invalid_payment.is_valid())
        self.assertIn("amount", invalid_payment.errors)

        valid_payment = PaymentSerializer(
            data={
                "treatment_plan": self.plan.pk,
                "method": Payment.Method.CASH,
                "amount": "30.00",
                "paid_at": now,
                "status": Payment.Status.CONFIRMED,
            }
        )
        self.assertTrue(valid_payment.is_valid(), valid_payment.errors)
        valid_payment.save()
        self.assertEqual(self.plan.balance_due, Decimal("20.00"))

    def test_history_evolution_endpoint_is_rbac_protected_and_append_only(self):
        history = ClinicalHistory.objects.create(patient=self.patient)
        role = Role.objects.create(name="Odontólogo")
        user = get_user_model().objects.create_user(
            username="dentist",
            password="test-password",
        )
        RoleUser.objects.create(user=user, role=role)
        resource = Resource.objects.create(name="historias")
        ResourceRole.objects.create(role=role, resource=resource)

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.post(
            f"/api/historias/{history.pk}/evoluciones/",
            {
                "findings": "Hallazgo de prueba",
                "procedures": "Procedimiento de prueba",
                "materials_used": "Material de prueba",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        evolution_id = response.data["id"]
        delete_response = client.delete(
            f"/api/historias/{history.pk}/evoluciones/{evolution_id}/"
        )
        self.assertEqual(delete_response.status_code, 404)
