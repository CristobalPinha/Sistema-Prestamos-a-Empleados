from django.test import TestCase
from django.utils import timezone
from django.forms import ValidationError
from rest_framework.test import APIClient
from .models import Comuna, Empleado, TipoPrestamo, Prestamo, Cuota
from .services import generar_cuotas
from .forms import validar_rut


# Datos reutilizables para todos los tests
def crear_empleado():
    comuna = Comuna.objects.create(nombre_comuna='Santiago')
    return Empleado.objects.create(
        RUT_empleado='12345678-9',
        nombre_empleado='Juan',
        apellido_empleado='Pérez',
        direccion_empleado='Av. Principal 123',
        Comuna=comuna,
    )

def crear_tipo_prestamo(tasa=10):
    return TipoPrestamo.objects.create(tipo_prestamo='Personal', tasa_de_interes=tasa)

def crear_prestamo(monto=100000, cuotas=5, tasa=10):
    empleado = crear_empleado()
    tipo = crear_tipo_prestamo(tasa)
    return Prestamo.objects.create(
        monto_prestamo=monto,
        cantidad_cuotas=cuotas,
        Empleado=empleado,
        TipoPrestamo=tipo,
    )


# ─── Tests de validación de RUT ──────────────────────────────────────────────

class ValidarRutTest(TestCase):

    def test_rut_valido(self):
        # 11111111-1 es un RUT con dígito verificador correcto
        self.assertEqual(validar_rut('11111111-1'), '11111111-1')

    def test_rut_valido_con_puntos(self):
        # Debe aceptar puntos y normalizarlos
        self.assertEqual(validar_rut('11.111.111-1'), '11111111-1')

    def test_rut_valido_con_dv_k(self):
        # 19654321-K: RUT cuyo dígito verificador es K (verificado con módulo 11)
        self.assertEqual(validar_rut('19654321-K'), '19654321-K')

    def test_rut_valido_con_dv_k_minuscula(self):
        # Debe aceptar k minúscula y normalizarla a K
        self.assertEqual(validar_rut('19654321-k'), '19654321-K')

    def test_rut_con_digito_verificador_incorrecto(self):
        with self.assertRaises(ValidationError):
            validar_rut('11111111-2')

    def test_rut_sin_guion(self):
        with self.assertRaises(ValidationError):
            validar_rut('111111111')

    def test_rut_con_letras_en_cuerpo(self):
        with self.assertRaises(ValidationError):
            validar_rut('1234AB78-9')

    def test_rut_con_dv_invalido(self):
        with self.assertRaises(ValidationError):
            validar_rut('11111111-X')


# ─── Tests de lógica del modelo Prestamo ─────────────────────────────────────

class PrestamoCalculoTest(TestCase):

    def test_monto_pagar_se_calcula_con_interes(self):
        # Arrange + Act
        prestamo = crear_prestamo(monto=100000, tasa=10)

        # Assert: 100000 + 10% = 110000
        self.assertEqual(prestamo.monto_pagar, 110000)

    def test_monto_pagar_con_tasa_cero(self):
        prestamo = crear_prestamo(monto=50000, tasa=0)

        # Sin interés, monto_pagar debe ser igual al monto original
        self.assertEqual(prestamo.monto_pagar, 50000)

    def test_monto_pagar_con_tasa_alta(self):
        prestamo = crear_prestamo(monto=200000, tasa=50)

        # 200000 + 50% = 300000
        self.assertEqual(prestamo.monto_pagar, 300000)


# ─── Tests de generar_cuotas ─────────────────────────────────────────────────

class GenerarCuotasTest(TestCase):

    def test_genera_cantidad_correcta_de_cuotas(self):
        prestamo = crear_prestamo(monto=100000, cuotas=5)
        generar_cuotas(prestamo)

        self.assertEqual(prestamo.cuotas.count(), 5)

    def test_monto_cuota_es_division_del_total(self):
        # 110000 / 5 cuotas = 22000 por cuota
        prestamo = crear_prestamo(monto=100000, cuotas=5, tasa=10)
        generar_cuotas(prestamo)

        primera_cuota = prestamo.cuotas.first()
        self.assertEqual(primera_cuota.monto_cuota, 22000)

    def test_cuotas_tienen_numeros_consecutivos(self):
        prestamo = crear_prestamo(cuotas=3)
        generar_cuotas(prestamo)

        numeros = list(prestamo.cuotas.values_list('numero_cuota', flat=True).order_by('numero_cuota'))
        self.assertEqual(numeros, [1, 2, 3])

    def test_fechas_vencimiento_separadas_30_dias(self):
        prestamo = crear_prestamo(cuotas=2)
        generar_cuotas(prestamo)

        cuotas = prestamo.cuotas.order_by('numero_cuota')
        diferencia = cuotas[1].cuota_fecha_vencimiento - cuotas[0].cuota_fecha_vencimiento

        self.assertEqual(diferencia.days, 30)

    def test_cuotas_creadas_sin_fecha_de_pago(self):
        prestamo = crear_prestamo(cuotas=3)
        generar_cuotas(prestamo)

        sin_pagar = prestamo.cuotas.filter(cuota_fecha_pago__isnull=True).count()
        self.assertEqual(sin_pagar, 3)


# ─── Tests de la API ──────────────────────────────────────────────────────────

class EmpleadoAPITest(TestCase):

    def setUp(self):
        # setUp se ejecuta antes de cada test, el cliente simula peticiones HTTP
        self.client = APIClient()
        self.empleado = crear_empleado()

    def test_listar_empleados_retorna_200(self):
        response = self.client.get('/api/empleados/')
        self.assertEqual(response.status_code, 200)

    def test_listar_empleados_retorna_datos(self):
        response = self.client.get('/api/empleados/')
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['RUT_empleado'], '12345678-9')

    def test_detalle_empleado_retorna_200(self):
        response = self.client.get('/api/empleados/12345678-9/')
        self.assertEqual(response.status_code, 200)

    def test_empleado_inexistente_retorna_404(self):
        response = self.client.get('/api/empleados/99999999-9/')
        self.assertEqual(response.status_code, 404)


class PrestamoAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.prestamo = crear_prestamo(monto=100000, cuotas=5)
        generar_cuotas(self.prestamo)

    def test_listar_prestamos_retorna_200(self):
        response = self.client.get('/api/prestamos/')
        self.assertEqual(response.status_code, 200)

    def test_detalle_prestamo_incluye_cuotas(self):
        response = self.client.get(f'/api/prestamos/{self.prestamo.id_prestamo}/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('cuotas', response.data)
        self.assertEqual(len(response.data['cuotas']), 5)

    def test_endpoint_cuotas_del_prestamo(self):
        response = self.client.get(f'/api/prestamos/{self.prestamo.id_prestamo}/cuotas/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
