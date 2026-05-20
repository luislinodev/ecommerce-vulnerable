import uuid
from django.db import models
from django.contrib.auth.models import User
from catalog.models import Catalog

class Order(models.Model):
    STATUS_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('cancelado', 'Cancelado'),
    ]
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # Información del evento
    event_date = models.DateField()
    address_text = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()
    phone = models.CharField(max_length=20)
    comments = models.TextField(blank=True, null=True)

    # Estado y aceptación
    accept_terms = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')

    # Costos
    transport_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    product_total = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    igv = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    total = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Orden #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Catalog, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        if self.product:
            return f"{self.quantity} x {self.product.name}"
        return f"{self.quantity} x Producto eliminado"
