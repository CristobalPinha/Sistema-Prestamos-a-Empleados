# Implementaciones aplicadas al proyecto

Mejoras realizadas al sistema original para dejarlo a nivel de portfolio profesional.

---

## 1. API REST

**Archivos:** `myapp/serializers.py` (nuevo), `myapp/views.py`, `mysite/urls.py`, `mysite/settings.py`

Se expuso una API REST bajo `/api/` usando Django REST Framework. Permite que cualquier cliente externo (app móvil, frontend en React, otro servidor) consuma los datos del sistema en formato JSON, independiente de la interfaz web.

Cada modelo tiene su propio serializer que convierte objetos de Django a JSON. Los ViewSets generan automáticamente las operaciones CRUD completas (listar, obtener, crear, editar, eliminar) con muy poco código. El Router registra todas las rutas automáticamente bajo `/api/`.

Los préstamos devuelven sus cuotas anidadas dentro del mismo JSON, y existe un endpoint extra `/api/prestamos/{id}/cuotas/` para obtenerlas por separado.

---

## 2. Tests automatizados

**Archivo:** `myapp/tests.py`

Se agregaron 26 tests automatizados ejecutables con `python manage.py test myapp`. Django crea una base de datos de prueba temporal y la destruye al terminar, sin tocar los datos reales.

| Grupo | Tests | Qué verifica |
|-------|-------|--------------|
| `ValidarRutTest` | 8 | Formato y dígito verificador del RUT chileno |
| `EstadoCuotaTest` | 3 | Los 3 estados posibles de una cuota |
| `PrestamoCalculoTest` | 3 | Cálculo del monto total con distintas tasas de interés |
| `GenerarCuotasTest` | 5 | Cantidad, monto, numeración, fechas y estado inicial |
| `EmpleadoAPITest` | 4 | Endpoints de empleados |
| `PrestamoAPITest` | 3 | Endpoints de préstamos y cuotas anidadas |

---

## 3. Docker

**Archivos:** `Dockerfile`, `docker-compose.yml`, `.dockerignore`, `mysite/settings.py`

Se agregó soporte para Docker, permitiendo levantar el proyecto completo con un solo comando sin instalar Python ni MySQL manualmente.

```bash
docker compose up --build
```

El `docker-compose.yml` orquesta dos contenedores: Django y MySQL. Incluye un healthcheck que hace que Django espere a que MySQL esté completamente listo antes de arrancar. `DB_HOST` se lee desde variable de entorno para soportar ambos entornos:

| Entorno | `DB_HOST` |
|---------|-----------|
| Local | `localhost` |
| Docker | `db` |

---

## 4. Validación de RUT chileno

**Archivo:** `myapp/forms.py`

Se implementó la función `validar_rut()` usando el algoritmo Módulo 11, que verifica que el dígito verificador de un RUT chileno sea correcto. Se conecta al formulario de registro de empleados mediante `clean_RUT_empleado()`.

**Algoritmo Módulo 11:**
1. Tomar los dígitos del RUT de derecha a izquierda
2. Multiplicar por la secuencia `2, 3, 4, 5, 6, 7, 2, 3...`
3. Sumar todos los productos
4. Calcular `11 - (suma % 11)`
5. Si el resultado es `10` → dígito es `K`, si es `11` → dígito es `0`

Acepta RUTs con o sin puntos y normaliza `k` minúscula a `K` automáticamente.

---

## 5. Estado automático de cuotas

**Archivo:** `myapp/models.py`

Se agregó un `@property estado` al modelo `Cuota` que calcula el estado en tiempo real sin almacenarlo en la base de datos:

| Estado | Condición |
|--------|-----------|
| Pagada | Tiene fecha de pago registrada |
| Vencida | Sin fecha de pago y la fecha de vencimiento ya pasó |
| Al día | Sin fecha de pago y la fecha de vencimiento aún no llega |

El estado se muestra con colores en la tabla de cuotas (verde / rojo / azul) y se expone también en la API.

---

## 6. Marcar cuotas como pagadas

**Archivos:** `myapp/views.py`, `mysite/urls.py`, `myapp/templates/loan_detail.html`

Se agregó un botón "Marcar como pagada" en cada cuota pendiente del detalle del préstamo. Al hacer clic registra la fecha y hora actual como fecha de pago. El botón desaparece una vez que la cuota está pagada.

---

## 7. Sistema de aprobación de préstamos

**Archivos:** `myapp/models.py`, `myapp/views.py`, `mysite/urls.py`, `myapp/templates/loan_approvals.html`

Se agregó un campo `estado` al modelo `Prestamo` con tres valores posibles: `pendiente`, `aprobado` y `rechazado`. El flujo ahora es:

```
Crear préstamo → Pendiente
      ↓
Pestaña Aprobaciones → Aprobar / Rechazar
      ↓
Aprobado → se generan las cuotas automáticamente
Rechazado → sin cuotas
```

Las cuotas ya no se generan al crear el préstamo, sino solo al aprobarlo. La pestaña de Aprobaciones lista todos los préstamos pendientes con botones de acción.

---

## 8. Dashboard con métricas

**Archivos:** `myapp/views.py`, `myapp/templates/dashboard.html`, `mysite/urls.py`

Se reemplazó la página de inicio por un dashboard con 5 tarjetas de métricas calculadas en tiempo real:

| Tarjeta | Métrica |
|---------|---------|
| Empleados | Total de empleados registrados |
| Préstamos activos | Total de préstamos aprobados |
| Monto total prestado | Suma de montos de préstamos aprobados |
| Cuotas vencidas | Cuotas sin pagar con vencimiento pasado (rojo si hay alguna) |
| Préstamos pendientes | Préstamos esperando aprobación, con link directo a la pestaña |

---

## 9. Exportar a Excel y PDF

**Archivos:** `myapp/views.py`, `mysite/urls.py`, `myapp/templates/loan_detail.html`

Se agregaron dos botones en el detalle de cada préstamo aprobado para descargar las cuotas:

- **Excel** (`openpyxl`) — genera un `.xlsx` con encabezado del préstamo y tabla de cuotas
- **PDF** (`reportlab`) — genera un `.pdf` con título, datos del préstamo y tabla con colores

Los archivos se generan al instante y se descargan directamente sin guardar nada en el servidor.

---

## 10. Datos iniciales

**Archivos:** `myapp/migrations/0002_cargar_comunas_santiago.py`, `myapp/migrations/0003_cargar_tipos_prestamo.py`

Se crearon migraciones de datos que cargan automáticamente al correr `python manage.py migrate`:

- **35 comunas** de la Región Metropolitana de Santiago
- **6 tipos de préstamo** con tasas acordes a un sistema empresarial:

| Tipo | Tasa |
|------|------|
| Préstamo de Emergencia | 0% |
| Préstamo de Salud | 3% |
| Préstamo de Educación | 4% |
| Préstamo Personal | 5% |
| Préstamo de Vehículo | 7% |
| Préstamo de Vivienda | 8% |
