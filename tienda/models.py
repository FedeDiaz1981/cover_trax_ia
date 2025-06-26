from django.db import models

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    modelo_compatible = models.CharField(max_length=100)  # Hilux, Ranger, etc.
    material = models.CharField(max_length=50)            # Acero inoxidable, etc.
    tipo = models.CharField(max_length=50)                # Retráctil, Fijo, etc.
    garantia_anios = models.IntegerField()
    imagen = models.ImageField(upload_to='productos/')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.modelo_compatible})"

class Carrito(models.Model):
    productos = models.ManyToManyField(Producto, through='CarritoProducto')

class CarritoProducto(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)