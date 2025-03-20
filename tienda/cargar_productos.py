from tienda.models import Producto
from django.core.files.base import ContentFile
import requests
from io import BytesIO
import random

productos = [
    ("Guitarra Acústica Fender", "Sonido cálido y brillante con diseño clásico.", 250.99, "https://example.com/guitarra1.jpg"),
    ("Batería Yamaha", "Perfecta para rock y jazz, incluye platillos.", 799.99, "https://example.com/bateria1.jpg"),
    ("Teclado Casio 61 Teclas", "Ideal para principiantes y músicos avanzados.", 199.99, "https://example.com/teclado1.jpg"),
    ("Bajo Eléctrico Ibanez", "Cuerpo sólido, ideal para rock y funk.", 499.99, "https://example.com/bajo1.jpg"),
    ("Violín Stradivarius Réplica", "Sonido hermoso, ideal para estudiantes avanzados.", 349.99, "https://example.com/violin1.jpg"),
    ("Micrófono Shure SM58", "Favorito de cantantes y podcasters.", 99.99, "https://example.com/microfono1.jpg"),
    ("Saxofón Alto Yamaha", "Excelente para jazz y música clásica.", 599.99, "https://example.com/saxo1.jpg"),
    ("Amplificador Marshall 50W", "Poderoso sonido para guitarra eléctrica.", 299.99, "https://example.com/amplificador1.jpg"),
    ("Pedal de Efectos BOSS", "Reverb y delay de alta calidad.", 149.99, "https://example.com/pedal1.jpg"),
    ("Ukelele Mahalo", "Pequeño, ligero y con sonido cálido.", 89.99, "https://example.com/ukelele1.jpg"),
]

# Crear 30 productos con imágenes
for i in range(30):
    nombre, descripcion, precio, imagen_url = random.choice(productos)
    
    response = requests.get(imagen_url)
    if response.status_code == 200:
        img_data = BytesIO(response.content)
        img_file = ContentFile(img_data.read(), name=f"producto_{i+1}.jpg")
        
        producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, imagen=img_file)
        producto.save()
        print(f"Producto {i+1} agregado: {nombre}")
    else:
        print(f"Error al descargar imagen {imagen_url}")
