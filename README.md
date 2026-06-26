# Sistema de Préstamos a Empleados

Aplicación web desarrollada con Django para gestionar préstamos otorgados a empleados de una organización. Permite registrar empleados, crear préstamos con tipos de interés definidos, generar automáticamente las cuotas de pago y hacer seguimiento del estado de cada cuota.

## Funcionalidades

**Empleados**
- Registrar, editar y eliminar empleados
- Cada empleado se identifica por su RUT y tiene asociada una comuna

**Préstamos**
- Crear préstamos vinculados a un empleado y un tipo de préstamo
- El sistema calcula automáticamente el monto total aplicando la tasa de interés del tipo de préstamo seleccionado
- Al crear un préstamo se generan automáticamente todas las cuotas con fechas de vencimiento separadas por 30 días

**Cuotas**
- Ver el detalle de las cuotas de cada préstamo
- Registrar la fecha de pago de cada cuota para llevar el seguimiento

## API REST

La aplicación expone una API REST bajo el prefijo `/api/` construida con Django REST Framework.

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/empleados/` | Lista todos los empleados |
| GET | `/api/empleados/{rut}/` | Detalle de un empleado |
| POST | `/api/empleados/` | Crear un empleado |
| PUT | `/api/empleados/{rut}/` | Editar un empleado |
| DELETE | `/api/empleados/{rut}/` | Eliminar un empleado |
| GET | `/api/prestamos/` | Lista todos los préstamos |
| GET | `/api/prestamos/{id}/` | Detalle de un préstamo con sus cuotas |
| POST | `/api/prestamos/` | Crear un préstamo |
| DELETE | `/api/prestamos/{id}/` | Eliminar un préstamo |
| GET | `/api/prestamos/{id}/cuotas/` | Cuotas de un préstamo específico |
| GET | `/api/tipos-prestamo/` | Lista los tipos de préstamo |
| GET | `/api/comunas/` | Lista las comunas |

La interfaz navegable de DRF está disponible en `http://127.0.0.1:8000/api/`.

## Tests

El proyecto incluye 15 tests automatizados que verifican la lógica de negocio y los endpoints de la API.

```powershell
python manage.py test myapp --verbosity=2
```

**Formato de RUT aceptado:** con o sin puntos, con guión obligatorio. El dígito verificador puede ser un número del 0 al 9 o la letra K (mayúscula o minúscula). El sistema normaliza automáticamente al formato `12345678-9`.

```
Válido:   12345678-9   ✓
Válido:   12.345.678-9 ✓  (los puntos se eliminan automáticamente)
Válido:   19654321-K   ✓
Inválido: 123456789    ✗  (sin guión)
Inválido: 12345678-X   ✗  (dígito verificador inválido)
Inválido: 12345678-5   ✗  (dígito verificador incorrecto)
```

| Grupo | Tests | Qué verifica |
|-------|-------|--------------|
| `ValidarRutTest` | 8 | Formato y dígito verificador del RUT chileno (casos válidos e inválidos) |
| `PrestamoCalculoTest` | 3 | Cálculo correcto del monto total con distintas tasas de interés |
| `GenerarCuotasTest` | 5 | Cantidad, monto, numeración, fechas y estado inicial de las cuotas |
| `EmpleadoAPITest` | 4 | Endpoints de empleados: listado, detalle y 404 |
| `PrestamoAPITest` | 3 | Endpoints de préstamos: listado, cuotas anidadas y endpoint /cuotas/ |

## Tecnologías

- Python 3.14
- Django 5.0.6
- Django REST Framework 3.15.2
- MySQL
- PyMySQL (conector de base de datos)

## Requisitos previos

- Python 3.10 o superior
- MySQL 8.0 o superior con el servicio activo

## Instalación y ejecución

**1. Crear y activar el entorno virtual**
```powershell
python -m venv venvPE
.\venvPE\Scripts\Activate.ps1
```

**2. Instalar dependencias**
```powershell
pip install django==5.0.6 djangorestframework==3.15.2 PyMySQL python-dotenv
```

**3. Crear la base de datos en MySQL**
```sql
CREATE DATABASE prestamos_empleados CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**4. Aplicar las migraciones**
```powershell
python manage.py migrate
```

**5. Iniciar el servidor**
```powershell
python manage.py runserver
```

La aplicación queda disponible en `http://127.0.0.1:8000`.

## Configuración de la base de datos

Las credenciales de conexión se definen en un archivo `.env` en la raíz del proyecto:

```
DB_NAME=prestamos_empleados
DB_USER=root
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=3306
```

## Estructura del proyecto

```
Sistema-Prestamos-a-Empleados/
├── manage.py
├── mysite/          # Configuración principal del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── myapp/           # Aplicación principal
    ├── models.py    # Modelos: Empleado, Prestamo, Cuota, TipoPrestamo, Comuna
    ├── views.py     # Vistas y lógica de negocio
    ├── forms.py     # Formularios
    └── urls.py      # Rutas de la aplicación
```
