"""
URL configuration for proyectofinal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inmobilapp.views import (
    registro_usuario,
    index,detalle_inmueble,
    generar_solicitud_arriendo,
    solicitudes_arrendador,alta_inmueble,
    propiedades,
    about,
    actualizar_inmueble,
    eliminar_inmueble,
    dashboard,
    cambiar_estado_solicitud,
    actualizar_inmueble,
    actualizar_usuario,
    
    
)

from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static

from proyectofinal import settings 

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    
    #Registro y perfil de usuario
    path('registro/', registro_usuario, name='registro_usuario'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
  
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('about/',about,name='about'),
    path('perfil/', actualizar_usuario, name='actualizar_usuario'),
    
    #Path de Inmueble
    path('inmueble/<int:id>',detalle_inmueble , name='detalle'),
    path('inmuebles/<int:id>/generar-solicitud/', generar_solicitud_arriendo, name='generar_solicitud_arriendo'),
    path('inmueble/<int:id>/editar_inmueble',actualizar_inmueble, name='editar_inmueble'),
    path('inmueble/<int:id>/eliminar_inmueble',eliminar_inmueble, name='eliminar_inmueble'),
    path('dashboard/', dashboard, name='dashboard'),
    path('cambiar_estado_solicitud/<int:solicitud_id>/', cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
    path('perfil/',actualizar_usuario,name='perfil'),
    
    #Solicitudes
    path('propiedades/', propiedades, name='propiedades'),
    path('solicitudes/', solicitudes_arrendador, name='solicitudes_arrendador'),
    path('alta-inmueble/', alta_inmueble, name='alta_inmueble'),
    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

