

# Create your views here.
from rest_framework import viewsets, permissions
from security.permissions import HasResourcePermission
from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, HasResourcePermission]
    resource_name = 'pacientes'
