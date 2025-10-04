# Usamos Nginx para servir el sitio estático
FROM nginx:alpine

# Copiar archivos del frontend al directorio de Nginx
COPY . /usr/share/nginx/html

# Exponer puerto 80
EXPOSE 80

# Comando de inicio
CMD ["nginx", "-g", "daemon off;"]
