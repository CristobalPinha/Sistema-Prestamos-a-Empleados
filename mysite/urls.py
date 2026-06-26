from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from myapp import views

# El Router genera estas URLs automáticamente por cada ViewSet registrado:
#   GET    /api/empleados/          → lista todos
#   POST   /api/empleados/          → crea uno nuevo
#   GET    /api/empleados/{rut}/    → detalle de uno
#   PUT    /api/empleados/{rut}/    → edita completo
#   PATCH  /api/empleados/{rut}/    → edita parcial
#   DELETE /api/empleados/{rut}/    → elimina
router = DefaultRouter()
router.register(r'empleados', views.EmpleadoViewSet)
router.register(r'prestamos', views.PrestamoViewSet)
router.register(r'tipos-prestamo', views.TipoPrestamoViewSet)
router.register(r'comunas', views.ComunaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Todos los endpoints bajo /api/
    path('', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<str:RUT_empleado>/update/', views.employee_update, name='employee_update'),
    path('employees/<str:RUT_empleado>/delete/', views.employee_delete, name='employee_delete'),
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/create/', views.loan_create, name='loan_create'),
    path('loans/<int:id_prestamo>/', views.loan_detail, name='loan_detail'),
    path('loans/<int:id_prestamo>/delete/', views.loan_delete, name='loan_delete'),
]
