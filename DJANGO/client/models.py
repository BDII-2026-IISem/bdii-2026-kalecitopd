from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username


class Patient(models.Model):
    document_type = models.CharField(max_length=30, verbose_name="Tipo de documento")
    document_number = models.CharField(
        max_length=30,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Número de documento",
    )
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")
    date_of_birth = models.DateField(
        blank=True, null=True, verbose_name="Fecha de nacimiento"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "client_client"
        verbose_name = "Paciente"
        verbose_name_plural = "Pacientes"
        ordering = ['-created_at']