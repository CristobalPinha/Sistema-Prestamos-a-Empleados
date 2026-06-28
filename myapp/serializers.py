from rest_framework import serializers
from .models import Comuna, Empleado, TipoPrestamo, Prestamo, Cuota


class ComunaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comuna
        fields = ['id_comuna', 'nombre_comuna']


class EmpleadoSerializer(serializers.ModelSerializer):
    # Sin esto, la API devolvería solo el ID de la comuna (ej: 3)
    # Con esto, devuelve el nombre completo (ej: "Santiago")
    comuna_nombre = serializers.CharField(source='Comuna.nombre_comuna', read_only=True)

    class Meta:
        model = Empleado
        fields = ['RUT_empleado', 'nombre_empleado', 'apellido_empleado', 'direccion_empleado', 'Comuna', 'comuna_nombre']


class TipoPrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoPrestamo
        fields = ['id_tipo_prestamo', 'tipo_prestamo', 'tasa_de_interes']


class CuotaSerializer(serializers.ModelSerializer):
    # read_only=True porque es un @property, no un campo de la base de datos
    estado = serializers.CharField(read_only=True)

    class Meta:
        model = Cuota
        fields = ['id_cuota', 'numero_cuota', 'monto_cuota', 'cuota_fecha_vencimiento', 'cuota_fecha_pago', 'estado']


class PrestamoSerializer(serializers.ModelSerializer):
    # Incluye todas las cuotas del préstamo dentro del mismo JSON
    # many=True porque un préstamo tiene varias cuotas
    cuotas = CuotaSerializer(many=True, read_only=True)

    # Igual que con empleado: muestra el nombre en vez del ID
    empleado_nombre = serializers.CharField(source='Empleado.__str__', read_only=True)
    tipo_prestamo_nombre = serializers.CharField(source='TipoPrestamo.tipo_prestamo', read_only=True)

    class Meta:
        model = Prestamo
        fields = [
            'id_prestamo', 'monto_prestamo', 'monto_pagar', 'cantidad_cuotas',
            'Empleado', 'empleado_nombre',
            'TipoPrestamo', 'tipo_prestamo_nombre',
            'cuotas',
        ]
