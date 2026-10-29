from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from security.permissions import HasResourcePermission

from .models import (
    Appointment,
    Chair,
    ClinicalHistory,
    ClinicalSession,
    Odontologist,
    Payment,
    Procedure,
    TreatmentDetail,
    TreatmentPlan,
)
from .serializers import (
    AppointmentSerializer,
    ChairSerializer,
    ClinicalEvolutionSerializer,
    ClinicalHistorySerializer,
    ClinicalSessionSerializer,
    OdontologistSerializer,
    PaymentSerializer,
    ProcedureSerializer,
    TreatmentDetailSerializer,
    TreatmentPlanSerializer,
)


class DentalViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, HasResourcePermission)


class OdontologistViewSet(DentalViewSet):
    queryset = Odontologist.objects.all()
    serializer_class = OdontologistSerializer
    resource_name = "odontologos"


class ChairViewSet(DentalViewSet):
    queryset = Chair.objects.all()
    serializer_class = ChairSerializer
    resource_name = "sillones"


class AppointmentViewSet(DentalViewSet):
    queryset = Appointment.objects.select_related("patient", "odontologist", "chair")
    serializer_class = AppointmentSerializer
    resource_name = "citas"
    http_method_names = ("get", "post", "put", "patch", "head", "options")


class ClinicalHistoryViewSet(DentalViewSet):
    queryset = ClinicalHistory.objects.select_related("patient").prefetch_related(
        "evolutions"
    )
    serializer_class = ClinicalHistorySerializer
    resource_name = "historias"
    http_method_names = ("get", "post", "put", "patch", "head", "options")

    @action(detail=True, methods=("post",), url_path="evoluciones")
    def evolutions(self, request, pk=None):
        history = self.get_object()
        serializer = ClinicalEvolutionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        evolution = serializer.save(
            clinical_history=history,
            created_by=request.user,
        )
        return Response(
            ClinicalEvolutionSerializer(evolution).data,
            status=status.HTTP_201_CREATED,
        )


class TreatmentPlanViewSet(DentalViewSet):
    queryset = TreatmentPlan.objects.select_related("patient").prefetch_related(
        "details"
    )
    serializer_class = TreatmentPlanSerializer
    resource_name = "tratamientos"


class ProcedureViewSet(DentalViewSet):
    queryset = Procedure.objects.all()
    serializer_class = ProcedureSerializer
    resource_name = "procedimientos"


class TreatmentDetailViewSet(DentalViewSet):
    queryset = TreatmentDetail.objects.select_related("treatment_plan", "procedure")
    serializer_class = TreatmentDetailSerializer
    resource_name = "detalles-tratamiento"


class ClinicalSessionViewSet(DentalViewSet):
    queryset = ClinicalSession.objects.select_related(
        "appointment",
        "appointment__patient",
        "treatment_plan",
    ).prefetch_related("executed_treatments__treatment_detail__procedure")
    serializer_class = ClinicalSessionSerializer
    resource_name = "sesiones"
    http_method_names = ("get", "post", "put", "patch", "head", "options")


class PaymentViewSet(DentalViewSet):
    queryset = Payment.objects.select_related("treatment_plan", "treatment_plan__patient")
    serializer_class = PaymentSerializer
    resource_name = "pagos"
    http_method_names = ("get", "post", "put", "patch", "head", "options")
