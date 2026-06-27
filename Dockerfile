# Imagen base: Python 3.12 slim (versión ligera, sin extras innecesarios)
# Usamos 3.12 en vez de 3.14 porque aún no hay imagen oficial de 3.14 en Docker Hub
FROM python:3.12-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias primero (antes del código)
# Esto aprovecha la caché de Docker: si requirements.txt no cambia,
# no reinstala nada aunque el código sí haya cambiado
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Puerto que expone el contenedor
EXPOSE 8000

# Comando que se ejecuta al iniciar el contenedor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
