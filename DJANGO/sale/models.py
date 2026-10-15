from django.db import models

# Create your models here.
from django.db import models
from client.models import Client
from product.models import Product

class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Cliente")
    date_issued = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Venta")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Monto Total")
    is_paid = models.BooleanField(default=False, verbose_name="Pagado")

    def __str__(self):
        return f"Venta #{self.id} - {self.client}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        ordering = ['-date_issued']

class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, related_name='details', on_delete=models.CASCADE, verbose_name="Venta")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Producto / Insumo")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Cantidad")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Subtotal")

    def __str__(self):
        return f"{self.quantity}x {self.product.name} (Venta #{self.sale.id})"

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"