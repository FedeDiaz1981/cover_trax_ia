from django.contrib import admin
from .models import Producto, Carrito, CarritoProducto

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio',"imagen")
    search_fields = ('nombre',)

@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    pass

@admin.register(CarritoProducto)
class CarritoProductoAdmin(admin.ModelAdmin):
    pass