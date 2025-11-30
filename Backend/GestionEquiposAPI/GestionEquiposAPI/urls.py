"""
URL configuration for GestionEquiposAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Equipos
    path('api/equipos/', include('APIEquipos.urls_equipos')),

    # Servicios
    path('api/servicio/', include('APIEquipos.urls_servicio')),

    # Ubicaciones
    path('api/ubicacion/', include('APIEquipos.urls_ubicacion')),

    #Sedes
    path('api/sedes/', include('APIEquipos.urls_sedes')),

    #Historial
    path('api/historial/', include('APIEquipos.urls_historial')),

    #Documentos
    path('api/documentos/', include('APIEquipos.urls_documento')),

    #Metro admin
    path('api/metrologia_adm/', include('APIEquipos.urls_metrologia')),

    #Metro tecnica
    path('api/metrologia_tec/', include('APIEquipos.urls_tecnica')),

    #Funcionamiento
    path('api/funcionamiento/', include('APIEquipos.urls_funcionamiento')),

    #Login
    path('api/login/', include('APILogin.urls')),

    #Detailed
    path('api/detailed/', include('APIEquipos.urls_detailed')),

    path("api/estadisticas/", include("APIEquipos.urls_estadisticas")),
    path("api/autocomplete/", include("APIEquipos.urls_autocomplete")),

    path("api/descargar/", include("APIEquipos.urls_descargar")),
    path("api/dar_baja/", include("APIEquipos.urls_darDebaja")),

]
