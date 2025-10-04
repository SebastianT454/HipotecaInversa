# Calculadora Hipoteca Inversa

## Autores
## Integrantes
## Tecnologías utilizadas
## Estructura del proyecto
## Instalación y ejecución
## Pruebas

#Calculadora Hipoteca Inversa

Este proyecto implementa un *simulador de hipoteca inversa* con arquitectura cliente-servidor. Incluye un *backend en Flask (Python), un **frontend en HTML/JS/CSS, y se puede ejecutar fácilmente con **Docker Compose*.

---

##Autores

Proyecto desarrollado como simulador de *hipoteca inversa*, integrando conceptos de finanzas, programación y despliegue con contenedores.

##Integrantes
-Sebastián Tamayo.
-Isabella Ceballos.
-Sofia Correa.

##Tecnologías utilizadas

* *Backend*: Python 3, Flask
* *Frontend*: HTML, CSS, JavaScript
* *Base de datos*: SQL (scripts incluidos)
* *Contenedores*: Docker y Docker Compose

---

##Estructura del proyecto


HipotecaInversa/
│── docker-compose.yml          # Orquestación con Docker
│
├── backend/                    # Lógica del servidor
│   ├── src/
│   │   ├── app.py              # Punto de entrada Flask
│   │   ├── ReverseMortgage/    # Cálculo de hipoteca inversa
│   │   ├── controller/         # Controladores de usuario
│   │   └── model/              # Modelos de datos
│   ├── tests/                  # Pruebas unitarias
│   ├── requirements.txt        # Dependencias Python
│   └── Dockerfile              # Imagen backend
│
├── frontend/                   # Interfaz de usuario
│   ├── index.html
│   ├── script.js
│   ├── styles.css
│   └── Dockerfile
│
└── ReverseMortgageSimulatorOriginal/  # Versión anterior del simulador


---

## Instalación y ejecución

### Opción 1: Con Docker

1. Clonar este repositorio:

   bash
   git clone https://github.com/SebastianT454/HipotecaInversa.git
   cd HipotecaInversa
   
2. Levantar los servicios:

   bash
   docker-compose up --build
   
3. Acceder a la app en:

   
   http://localhost:8080
   

### 🔹 Opción 2: Manual (sin Docker)

1. Instalar dependencias del backend:

   bash
   cd backend
   pip install -r requirements.txt
   python src/app.py
   
2. Abrir el frontend desde frontend/index.html.

---

## Pruebas

Ejecutar las pruebas del backend con:

bash
cd backend
pytest tests/


---



