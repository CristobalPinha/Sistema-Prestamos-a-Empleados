"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.listar_empleado, name='listar_empleado'),
    path('registrar_empleado/', views.registrar_empleado, name='registrar_empleado'),
    path('actualizar/<str:RUT_empleado>/', views.actualizar_empleado, name='actualizar_empleado'),
    path('eliminar/<str:RUT_empleado>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('crear_prestamo/', views.crear_prestamo, name='crear_prestamo'),
    path('detalle_prestamo/<int:id_prestamo>/', views.detalle_prestamo, name='detalle_prestamo'),
    path('listar_prestamo/', views.listar_prestamo, name='listar_prestamo'),
    path('eliminar_prestamo/<int:id_prestamo>/', views.eliminar_prestamo, name='eliminar_prestamo'),
]
