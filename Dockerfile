FROM python:3.11-slim

WORKDIR /app

# Copiar el código fuente y base de datos
COPY . /app

# Generar interfaz estática actualizada
RUN python crm/build_dashboard.py

# Exponer el puerto
EXPOSE 8500

# Variables de entorno por defecto
ENV PORT=8500
ENV PYTHONUNBUFFERED=1
ENV ADMIN_PIN=2026
ENV STAFF_PIN=1234

# Ejecutar el servidor CRM
CMD ["python", "crm/server.py"]
