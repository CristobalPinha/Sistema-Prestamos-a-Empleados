from datetime import timedelta
from django.utils import timezone
from .models import Cuota


def generar_cuotas(prestamo):
    monto_cuota = prestamo.monto_pagar // prestamo.cantidad_cuotas
    fecha_emision = timezone.now()

    cuotas = []
    for i in range(1, prestamo.cantidad_cuotas + 1):
        fecha_vencimiento = fecha_emision + timedelta(days=30 * i)
        cuotas.append(Cuota(
            Prestamo=prestamo,
            numero_cuota=i,
            monto_cuota=monto_cuota,
            cuota_fecha_emision=fecha_emision,
            cuota_fecha_vencimiento=fecha_vencimiento,
            cuota_fecha_pago=None,
        ))

    Cuota.objects.bulk_create(cuotas)
