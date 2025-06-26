from django.urls import path
from .views import * #tienda, cargar_productos, detalle_producto_ajax, obtener_total_carrito, agregar_al_carrito, obtener_productos 
#from .views import quitar_del_carrito, actualizar_carrito, ver_carrito, vaciar_carrito, confirmar_compra, chat_ia
from django.conf import settings
from django.conf.urls.static import static
from . import views_admin
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', tienda, name='tienda'),
    path('api/productos/', cargar_productos, name='cargar_productos'),
    path("detalle-producto/<int:producto_id>/", detalle_producto_ajax, name="detalle_producto_ajax"),
    path('actualizar_carrito/<int:producto_id>/', actualizar_carrito, name='actualizar_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('ver-carrito/', ver_carrito, name='ver_carrito'),
    path('agregar-al-carrito/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar-del-carrito/<int:producto_id>/', quitar_del_carrito, name='quitar_del_carrito'),
    path('vaciar-carrito/', vaciar_carrito, name='vaciar_carrito'),
    path("confirmar-compra/", confirmar_compra, name="confirmar_compra"),
    path("chat-ia/", chat_ia, name="chat_ia"),
    path("obtener-total-carrito/", obtener_total_carrito, name="obtener_total_carrito"),
    path('obtener-productos/', obtener_productos, name='obtener_productos'),
    path('admin-productos/', views_admin.admin_productos, name='admin_productos'),
    path('admin-productos/agregar/', views_admin.agregar_producto, name='agregar_producto'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('admin-productos/editar/<int:producto_id>/', views_admin.editar_producto, name='editar_producto'),
    path('admin-productos/eliminar/<int:producto_id>/', views_admin.eliminar_producto, name='eliminar_producto'),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
