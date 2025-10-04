# Imagen base de Python
FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /usr/src/app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . .

# Exponer el puerto donde corre el backend (ajusta si es distinto)
EXPOSE 5000

# Comando de inicio (ejecuta app.py dentro de src)
CMD ["python", "src/app.py"]
