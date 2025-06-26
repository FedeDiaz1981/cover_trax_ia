from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Producto
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages

@login_required(login_url='/login/')
def admin_productos(request):
    if not request.user.is_staff:
        messages.error(request, "No tenés permisos para acceder a esta sección.")
        return redirect('/')
    productos = Producto.objects.all()
    return render(request, 'tienda/admin_productos.html', {'productos': productos})

@login_required(login_url='/login/')
def agregar_producto(request):
    if not request.user.is_staff:
        messages.error(request, "No tenés permisos para acceder a esta sección.")
        return redirect('/')

# Solo admins
def es_admin(user):
    return user.is_staff

@user_passes_test(es_admin)
def admin_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tienda/admin_productos.html', {'productos': productos})

@user_passes_test(es_admin)
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_productos')
    else:
        form = ProductoForm()
    return render(request, 'tienda/agregar_producto.html', {'form': form})

@login_required(login_url='/login/')
def editar_producto(request, producto_id):
    if not request.user.is_staff:
        messages.error(request, "No tenés permisos para acceder a esta sección.")
        return redirect('/')
    
    producto = Producto.objects.get(id=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado correctamente.")
            return redirect('admin_productos')
    else:
        form = ProductoForm(instance=producto)
    
    return render(request, 'tienda/agregar_producto.html', {'form': form, 'modo_edicion': True})

@login_required(login_url='/login/')
def eliminar_producto(request, producto_id):
    if not request.user.is_staff:
        messages.error(request, "No tenés permisos para acceder a esta sección.")
        return redirect('/')

    producto = Producto.objects.get(id=producto_id)
    producto.delete()
    messages.success(request, "Producto eliminado.")
    return redirect('admin_productos')
