from django.contrib import admin

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


@admin.register(Odontologist)
class OdontologistAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "odontologist",
        "chair",
        "start_time",
        "end_time",
        "status",
    )
    list_filter = ("status", "start_time", "odontologist", "chair")
    search_fields = (
        "patient__first_name",
        "patient__last_name",
        "patient__document_number",
        "motive",
    )
    autocomplete_fields = ("patient", "odontologist", "chair")

    def has_delete_permission(self, request, obj=None):
        return False


class ClinicalEvolutionInline(admin.TabularInline):
    model = ClinicalEvolution
    extra = 0
    can_delete = False
    readonly_fields = (
        "findings",
        "procedures",
        "materials_used",
        "consent_signed_at",
        "created_by",
        "created_at",
    )


@admin.register(ClinicalHistory)
class ClinicalHistoryAdmin(admin.ModelAdmin):
    list_display = ("patient", "name", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("patient__first_name", "patient__last_name", "description")
    autocomplete_fields = ("patient",)
    inlines = (ClinicalEvolutionInline,)

    def has_delete_permission(self, request, obj=None):
        return False


class TreatmentDetailInline(admin.TabularInline):
    model = TreatmentDetail
    extra = 0
    readonly_fields = ("total",)
    autocomplete_fields = ("procedure",)


@admin.register(TreatmentPlan)
class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "patient", "status", "total_amount", "balance_due")
    list_filter = ("status", "created_at")
    search_fields = ("name", "patient__first_name", "patient__last_name")
    autocomplete_fields = ("patient",)
    inlines = (TreatmentDetailInline,)

    @admin.display(description="Total")
    def total_amount(self, obj):
        return obj.total_amount

    @admin.display(description="Saldo pendiente")
    def balance_due(self, obj):
        return obj.balance_due


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "description")


@admin.register(TreatmentDetail)
class TreatmentDetailAdmin(admin.ModelAdmin):
    list_display = (
        "treatment_plan",
        "procedure",
        "quantity",
        "approved_quantity",
        "unit_price",
        "total",
    )
    list_filter = ("procedure",)
    search_fields = ("treatment_plan__name", "procedure__name")
    autocomplete_fields = ("treatment_plan", "procedure")
    readonly_fields = ("total",)


class SessionTreatmentInline(admin.TabularInline):
    model = SessionTreatment
    extra = 0
    can_delete = False
    autocomplete_fields = ("treatment_detail",)


@admin.register(ClinicalSession)
class ClinicalSessionAdmin(admin.ModelAdmin):
    list_display = (
        "appointment",
        "treatment_plan",
        "start_time",
        "end_time",
        "total",
        "status",
    )
    list_filter = ("status", "start_time")
    search_fields = (
        "appointment__patient__first_name",
        "appointment__patient__last_name",
        "treatment_plan__name",
    )
    autocomplete_fields = ("appointment", "treatment_plan")
    readonly_fields = ("total",)
    inlines = (SessionTreatmentInline,)

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("treatment_plan", "method", "amount", "paid_at", "status")
    list_filter = ("method", "status", "paid_at")
    search_fields = ("treatment_plan__name", "treatment_plan__patient__last_name")
    autocomplete_fields = ("treatment_plan",)

    def has_delete_permission(self, request, obj=None):
        return False
