Calculadora-HI Web (Flask + Frontend)
====================================

Estructura:
- backend/app.py     -> Flask app que expone /calculate y sirve el frontend
- backend/requirements.txt
- frontend/index.html, styles.css, script.js

Cómo correr:
1. Crear y activar un entorno virtual (recomendado):
   python -m venv venv
   source venv/bin/activate   (Linux/Mac)  o  venv\Scripts\activate  (Windows)

2. Instalar dependencias:
   pip install -r backend/requirements.txt

3. Ejecutar:
   cd backend
   python app.py

4. Abrir en el navegador:
   http://127.0.0.1:5000/

Notas:
- Implementé una función `safe_eval` en backend/app.py que evalúa expresiones matemáticas básicas y funciones de math.
- Si tu proyecto original contiene lógica específica (por ejemplo historial, funciones avanzadas), la he dejado dentro del directorio extraído. Puedes copiar funciones concretas desde los archivos originales a backend/app.py para preservar comportamiento exacto.