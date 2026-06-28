# LendIn

Plataforma web para gestionar préstamos otorgados a empleados de una organización. Desarrollada con Django, incluye un panel de administración con dashboard, flujo de aprobación, seguimiento de cuotas y API REST.

## Funcionalidades

**Dashboard**
- Métricas en tiempo real: solicitudes pendientes, cuotas vencidas, préstamos activos y capital total prestado
- Tabla de solicitudes recientes con acciones de aprobación directa

**Empleados**
- Registrar, editar y eliminar empleados
- Validación de RUT chileno con algoritmo Módulo 11
- 35 comunas de la Región Metropolitana precargadas

**Préstamos**
- Flujo de aprobación: las solicitudes quedan pendientes hasta ser aprobadas o rechazadas
- Al aprobar se generan automáticamente las cuotas con fechas de vencimiento cada 30 días
- 6 tipos de préstamo con tasas definidas (Emergencia 0%, Salud 3%, Educación 4%, Personal 5%, Vehículo 7%, Vivienda 8%)

**Cuotas**
- Estado automático: Pagada / Al día / Vencida calculado en tiempo real
- Registro de fecha de pago por cuota
- Exportar detalle a Excel o PDF

**Autenticación**
- Acceso restringido a personal autorizado
- Login con diseño LendIn, logout desde el sidebar
- Usuarios gestionados desde `/admin/` o `createsuperuser`

**Búsqueda y filtros**
- Empleados: búsqueda en tiempo real por nombre, apellido o RUT
- Préstamos: filtro por estado (Pendiente / Aprobado / Rechazado)
- Paginación de 10 registros por página en ambas listas

**Panel de administración**
- `/admin/` con diseño personalizado en colores LendIn
- Gestión de usuarios, empleados, préstamos, cuotas, tipos y comunas

**API REST**
- Endpoints completos bajo `/api/` para todos los modelos
- Interfaz navegable de Django REST Framework

## API REST

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/empleados/` | Lista todos los empleados |
| GET/PUT/DELETE | `/api/empleados/{rut}/` | Detalle, editar o eliminar |
| POST | `/api/empleados/` | Crear empleado |
| GET | `/api/prestamos/` | Lista todos los préstamos |
| GET/DELETE | `/api/prestamos/{id}/` | Detalle con cuotas o eliminar |
| POST | `/api/prestamos/` | Crear préstamo |
| GET | `/api/prestamos/{id}/cuotas/` | Cuotas de un préstamo |
| GET | `/api/tipos-prestamo/` | Lista tipos de préstamo |
| GET | `/api/comunas/` | Lista comunas |

Interfaz navegable disponible en `http://127.0.0.1:8000/api/`.

## Tests

26 tests automatizados ejecutables con:

```bash
python manage.py test myapp --verbosity=2
```

| Grupo | Tests | Qué verifica |
|-------|-------|--------------|
| `ValidarRutTest` | 8 | Formato y dígito verificador del RUT |
| `EstadoCuotaTest` | 3 | Estados Pagada / Vencida / Al día |
| `PrestamoCalculoTest` | 3 | Cálculo del monto total con interés |
| `GenerarCuotasTest` | 5 | Cantidad, montos, fechas y numeración |
| `EmpleadoAPITest` | 4 | Endpoints de empleados |
| `PrestamoAPITest` | 3 | Endpoints de préstamos y cuotas |

**Validación de RUT:** acepta con o sin puntos, normaliza `k` a `K`.
```
Válido:   12345678-9    Válido:   12.345.678-9    Válido: 19654321-K
Inválido: 123456789     Inválido: 12345678-X      Inválido: 12345678-5
```

## Tecnologías

- Python 3.14 · Django 5.0.6
- Django REST Framework 3.15.2
- MySQL 8.0 · PyMySQL
- openpyxl · ReportLab
- Docker y Docker Compose

## Instalación

### Con Docker (recomendado)

Requiere [Docker Desktop](https://www.docker.com/products/docker-desktop/).

```bash
# 1. Configurar .env
SECRET_KEY=django-insecure-...
DB_PASSWORD=1234
DB_HOST=db

# 2. Levantar
docker compose up

# 3. Apagar
docker compose down
```

La app queda disponible en `http://127.0.0.1:8000`. Las migraciones y datos iniciales se aplican automáticamente.

---

### Sin Docker

**Requisitos:** Python 3.10+ · MySQL 8.0+

```powershell
# 1. Entorno virtual
python -m venv venvPE
.\venvPE\Scripts\Activate.ps1

# 2. Dependencias
pip install -r requirements.txt

# 3. Base de datos en MySQL
CREATE DATABASE prestamos_empleados CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 4. Configurar .env
SECRET_KEY=django-insecure-...
DB_PASSWORD=1234
DB_HOST=localhost

# 5. Migraciones
python manage.py migrate

# 6. Servidor
python manage.py runserver
```

## Estructura del proyecto

```
LendIn/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── mysite/                  # Configuración principal
│   ├── settings.py
│   └── urls.py
└── myapp/                   # Aplicación principal
    ├── models.py            # Empleado, Prestamo, Cuota, TipoPrestamo, Comuna
    ├── views.py             # Vistas web y API
    ├── serializers.py       # Serializers DRF
    ├── forms.py             # Formularios con validación de RUT
    ├── services.py          # Lógica de generación de cuotas
    ├── context_processors.py
    ├── migrations/          # Incluye datos iniciales de comunas y tipos
    ├── templates/           # Templates HTML
    └── static/              # CSS
```
