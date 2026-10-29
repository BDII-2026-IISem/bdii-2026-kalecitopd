from rest_framework.routers import DefaultRouter

from .views import (
    AppointmentViewSet,
    ChairViewSet,
    ClinicalHistoryViewSet,
    ClinicalSessionViewSet,
    OdontologistViewSet,
    PaymentViewSet,
    ProcedureViewSet,
    TreatmentDetailViewSet,
    TreatmentPlanViewSet,
)

router = DefaultRouter()
router.register("odontologos", OdontologistViewSet, basename="odontologist")
router.register("sillones", ChairViewSet, basename="chair")
router.register("citas", AppointmentViewSet, basename="appointment")
router.register("historias", ClinicalHistoryViewSet, basename="clinical-history")
router.register("tratamientos", TreatmentPlanViewSet, basename="treatment-plan")
router.register("procedimientos", ProcedureViewSet, basename="procedure")
router.register(
    "detalles-tratamiento",
    TreatmentDetailViewSet,
    basename="treatment-detail",
)
router.register("sesiones", ClinicalSessionViewSet, basename="clinical-session")
router.register("pagos", PaymentViewSet, basename="payment")

urlpatterns = router.urls
