class Carrito:
    def __init__(self, request):
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {'cantidad': 0, 'precio': str(producto.precio)}
        self.carrito[producto_id]['cantidad'] += cantidad
        self.save()

    def save(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True