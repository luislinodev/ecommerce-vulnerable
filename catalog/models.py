from django.db import models
from django.utils.text import slugify

class Catalog(models.Model):
    CATEGORIES = [
        ('mobiliario', 'Mobiliario'),
        ('vajilla', 'Vajilla y utensilios'),
        ('decoracion', 'Decoración'),
        ('iluminacion', 'Iluminación y sonido'),
        ('entretenimiento', 'Entretenimiento'),
        ('comida_bebidas', 'Comida y bebidas'),
        ('infraestructura', 'Infraestructura'),
        ('tematica', 'Temática y personalizados'),
        ('limpieza', 'Limpieza y desecho'),
        ('servicios', 'Otros servicios'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image_url = models.URLField(
        max_length=500,
        blank=True,
        help_text="Pega aquí el link directo a la imagen del producto (por ejemplo, desde Cloudinary)"
    )
    categories = models.CharField(
        max_length=50,
        choices=CATEGORIES,
        default='servicios',
        help_text="Selecciona la categoría del producto"
    )

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)  # Convierte el nombre en un slug
        super().save(*args, **kwargs)