from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.employee_list, name='employee_list'),
    path('employees/create/', views.employee_create, name='employee_create'),
    path('employees/<str:RUT_empleado>/update/', views.employee_update, name='employee_update'),
    path('employees/<str:RUT_empleado>/delete/', views.employee_delete, name='employee_delete'),
    path('loans/', views.loan_list, name='loan_list'),
    path('loans/create/', views.loan_create, name='loan_create'),
    path('loans/<int:id_prestamo>/', views.loan_detail, name='loan_detail'),
    path('loans/<int:id_prestamo>/delete/', views.loan_delete, name='loan_delete'),
]
