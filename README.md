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

## Tecnologías

- Python 3.14
- Django 5.0.6
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
