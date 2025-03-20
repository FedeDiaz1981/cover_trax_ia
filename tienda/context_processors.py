from decimal import Decimal

def carrito_total(request):
    carrito = request.session.get('carrito', {})
    total = sum(Decimal(item['precio']) * item['cantidad'] for item in carrito.values())
    return {'total': total}