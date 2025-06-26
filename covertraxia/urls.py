from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importamos las vistas de login/logout personalizadas
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App principal
    path('', include('tienda.urls')),

    # Login y logout personalizados
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
]

# Soporte para archivos multimedia (imágenes de productos)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
