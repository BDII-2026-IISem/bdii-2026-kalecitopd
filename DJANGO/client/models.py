from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Aquí puedes agregar campos adicionales para OdontoNova si los necesitas (ej. teléfono, rol, etc.)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username
    from django.db import models
from django.contrib.auth.models import AbstractUser

# Si ya tienes tu CustomUser definido, déjalo. Aquí añadimos el modelo Client:
class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name="Nombres")
    last_name = models.CharField(max_length=100, verbose_name="Apellidos")
    email = models.EmailField(unique=True, verbose_name="Correo Electrónico")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    address = models.TextField(blank=True, null=True, verbose_name="Dirección")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ['-created_at']