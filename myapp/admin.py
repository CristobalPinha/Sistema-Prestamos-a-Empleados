from django.contrib import admin
from .models import Empleado, Prestamo, Cuota, TipoPrestamo, Comuna

admin.site.site_header = "LendIn"
admin.site.site_title = "LendIn Admin"
admin.site.index_title = "Panel de Administración"


@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display  = ('RUT_empleado', 'nombre_empleado', 'apellido_empleado', 'Comuna', 'direccion_empleado')
    search_fields = ('RUT_empleado', 'nombre_empleado', 'apellido_empleado')
    list_filter   = ('Comuna',)
    ordering      = ('apellido_empleado', 'nombre_empleado')


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display  = ('id_prestamo', 'Empleado', 'TipoPrestamo', 'monto_prestamo', 'cantidad_cuotas', 'estado')
    list_filter   = ('estado', 'TipoPrestamo')
    search_fields = ('Empleado__nombre_empleado', 'Empleado__apellido_empleado', 'Empleado__RUT_empleado')
    ordering      = ('-id_prestamo',)


@admin.register(Cuota)
class CuotaAdmin(admin.ModelAdmin):
    list_display  = ('id_cuota', 'Prestamo', 'numero_cuota', 'monto_cuota', 'cuota_fecha_vencimiento', 'cuota_fecha_pago')
    list_filter   = ('cuota_fecha_pago',)
    ordering      = ('Prestamo', 'numero_cuota')


@admin.register(TipoPrestamo)
class TipoPrestamoAdmin(admin.ModelAdmin):
    list_display = ('tipo_prestamo', 'tasa_de_interes')


@admin.register(Comuna)
class ComunaAdmin(admin.ModelAdmin):
    list_display  = ('nombre_comuna',)
    search_fields = ('nombre_comuna',)
    ordering      = ('nombre_comuna',)
