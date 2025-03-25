from django.conf import settings
import google.generativeai as genai
from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Producto, Carrito, CarritoProducto
from django.contrib import messages


genai.configure(api_key=settings.GEMINI_API_KEY)

def tienda_view(request):
    productos = Producto.objects.all()
    carrito, _ = Carrito.objects.get_or_create(id=1)
    total = sum(item.producto.precio * item.cantidad for item in CarritoProducto.objects.filter(carrito=carrito))

    carrito_dict = {}
    for item in CarritoProducto.objects.filter(carrito=carrito):
        carrito_dict[str(item.producto.id)] = {'cantidad': item.cantidad, 'precio': str(item.producto.precio)}
    print("CarritoFD")
    print(carrito_dict)  # Agrega esta línea para depurar
    return render(request, 'tienda/tienda.html', {'productos': productos, 'total': total, 'carrito': carrito_dict})

def tienda(request):
    productos = Producto.objects.all()  # Obtener todos los productos de la base de datos
    carrito = request.session.get("carrito", {})

    total = sum(float(item["precio"]) * item["cantidad"] for item in carrito.values()) if carrito else 0

    context = {
        "productos": productos,
        "carrito_total": total
    }
    return render(request, "tienda/tienda.html", context)

def cargar_productos(request):
    productos = Producto.objects.all().values()
    return JsonResponse(list(productos), safe=False)

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    return render(request, "tienda/detalle_producto.html", {"producto": producto})

def detalle_producto_ajax(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Devolver la información del producto en JSON
    data = {
        "id": producto.id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": str(producto.precio),
        "imagen": producto.imagen.url if producto.imagen else "",
    }
    return JsonResponse(data)


def ver_carrito(request):
    carrito = request.session.get("carrito", {})
    total = sum(Decimal(item["precio"]) * item["cantidad"] for item in carrito.values()) if carrito else 0

    context = {
        "carrito": carrito,
        "carrito_total": total
    }
    return render(request, "tienda/carrito.html", context)



def agregar_al_carrito(request, producto_id):
    """ Agrega un producto al carrito con la cantidad seleccionada """
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get("cantidad", 1))

    carrito = request.session.get("carrito", {})

    if str(producto.id) in carrito:
        carrito[str(producto.id)]["cantidad"] += cantidad
    else:
        carrito[str(producto.id)] = {
            "nombre": producto.nombre,
            "precio": str(producto.precio),
            "cantidad": cantidad,
            "imagen": producto.imagen.url if producto.imagen else "",
        }

    request.session["carrito"] = carrito  # Guardar carrito en la sesión
    return JsonResponse({"success": True, "message": f"{producto.nombre} agregado al carrito."})



def quitar_del_carrito(request, producto_id):
    """Elimina un producto del carrito en sesión."""
    carrito = request.session.get('carrito', {})

    if str(producto_id) in carrito:
        del carrito[str(producto_id)]  # Borra el producto del diccionario
    
    request.session['carrito'] = carrito
    request.session.modified = True

    return redirect('ver_carrito')


def vaciar_carrito(request):
    """Elimina todos los productos del carrito."""
    request.session['carrito'] = {}
    request.session.modified = True
    return redirect('ver_carrito')



def actualizar_carrito(request, producto_id):
    if request.method == 'POST':
        producto = get_object_or_404(Producto, pk=producto_id)
        carrito, _ = Carrito.objects.get_or_create(id=1)
        cantidad = int(request.POST.get('cantidad', 1))

        # Lógica para actualizar la cantidad del producto en el carrito
        # ...

        return redirect('tienda')  # Redirige a la página de la tienda
    else:
        return redirect('tienda')  # Redirige si no es una solicitud POST

def obtener_total_carrito(request):
    """ Calcula el total del carrito y lo devuelve en JSON """
    carrito = request.session.get("carrito", {})
    total = sum(Decimal(item["precio"]) * item["cantidad"] for item in carrito.values()) if carrito else Decimal(0)
    
    return JsonResponse({"total": round(total, 2)})


def confirmar_compra(request):
    carrito = request.session.get("carrito", {})
    if not carrito:
        return redirect("ver_carrito")  # Si el carrito está vacío, redirigir

    total = sum(Decimal(item["precio"]) * item["cantidad"] for item in carrito.values())

    return render(request, "tienda/confirmar_compra.html", {
        "carrito": carrito,
        "carrito_total": round(total, 2),
    })

def chat_ia(request):
    if request.method == "POST":
        user_message = request.POST.get("message", "")

        try:
            # Llamar a Google Gemini 1.5 Pro para entender la intención del usuario
            model = genai.GenerativeModel("gemini-1.5-pro-001")
            response = model.generate_content(f"Dado este mensaje del usuario: '{user_message}', ¿qué tipo de producto musical podría necesitar? Responde solo con palabras clave separadas por comas, sin explicaciones.")

            # Extraer palabras clave de la respuesta de Gemini
            if hasattr(response, "text"):
                palabras_clave = [p.strip().lower() for p in response.text.split(",")]
            else:
                palabras_clave = []

        except Exception as e:
            print(f"Error en Google Gemini: {e}")
            palabras_clave = []

        # Filtrar productos en la base de datos en base a las palabras clave
        productos_filtrados = Producto.objects.none()  # Inicialmente vacío

        for palabra in palabras_clave:
            productos_coincidencia = Producto.objects.filter(nombre__icontains=palabra)
            productos_filtrados |= productos_coincidencia  # Agregar coincidencias

        # Limitar los productos recomendados a un máximo de 6
        productos_filtrados = productos_filtrados.distinct()[:6]

        # Convertir los productos a formato JSON
        productos_data = [{"id": p.id, "nombre": p.nombre, "precio": str(p.precio)} for p in productos_filtrados]

        return JsonResponse({
            "message": f"Te recomiendo estos productos según tu búsqueda: {', '.join(palabras_clave)}",
            "productos": productos_data
        })

    return JsonResponse({"error": "Método no permitido"}, status=405)

def obtener_productos(request):
    productos = Producto.objects.all()
    data = {
        "productos": [
            {
                "id": p.id,
                "nombre": p.nombre,
                "precio": float(p.precio),
                "imagen": p.imagen.url if p.imagen else "",
            }
            for p in productos
        ]
    }
    return JsonResponse(data)