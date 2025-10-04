# Proyecto Calculadora de Hipoteca Inversa

## Realizado por:

Samuel Gallego

Sofia Correa

## Propósito

Brindar una herramienta accesible y de fácil uso que permita a los usuarios evaluar de manera exhaustiva y precisa las opciones disponibles en el mercado de hipotecas inversas. Este software está diseñado para ayudar a los propietarios de viviendas de mayor edad a comprender cómo funciona este tipo de producto financiero, estimar la cantidad potencial de fondos que podrían recibir y visualizar el impacto que tendría una hipoteca inversa en su situación financiera a lo largo del tiempo. La calculadora ofrece una simulación interactiva basada en datos personalizados, lo que permite a los usuarios ajustar variables clave como el valor de la propiedad, la tasa de interés y la duración del préstamo.

## ¿Cómo funciona?

El usuario debe ingresar ciertos datos personales (edad, género, estado civil, edad de su cónyuge (opcional) y género de su cónyuge (opcional)). Adicionalmente, debe ingresar información relacionada con su vivienda y el financiamiento (valor y tasa de interés).

Posteriormente, el sistema se encargará de realizar los cálculos necesarios y devolverá el valor de cada cuota mensual de la hipoteca inversa.

## ¿Cómo se hace?

El proyecto se divide en dos carpetas principales, una carpeta `src` y una carpeta `tests`. La carpeta `src` contiene un módulo en el que se encuentra un archivo con la distribución de las clases y métodos, y otro es el módulo en el que se encuentra la ejecución del programa por consola. Por otro lado, la carpeta `tests` contiene cada uno de los `tests` unitarios (casos normales, casos extraordinarios y casos de error). Además, hay 3 archivos de la estructura general de un proyecto (.gitignore, README.md y License).

## Instalación y Uso de la base de datos

### Clonar el Repositorio:

Abre tu consola y ejecuta el siguiente comando:

    git clone "https://github.com/samdg441/ReverseMortgageSimulator.git"
  
### Cómo lo hago funcionar?

Prerrequisitos:

Asegurese de tener una base de datos PostgreSQL y sus respectivos datos de acceso

Copie el archivo Secret_Config-sample.py como Secret_Config.py y establezca en este archivo los datos de conexion a su base de datos.

Instale el paquete psycopg2 con: pip install psycopg2

### Cómo ejecutar los test

Para ejecutar los casos de prueba deberá de escrbir en la terminal de python los siguientes comandos:

Este ejecutará los casos de prueba para la calculadora de hipoteca inversa:
python tests/ReverseMortgageTests.py

Este ejecutará los casos de prueba para la base de datos:
python tests/DataBaseTests.py

### Navegar hasta el directorio del proyecto:

Cambie el directorio a la carpeta `ReverseMortgageSimulator`:

    cd path\to\ReverseMortgageSimulator

**Ejemplo:** Si clonara el repositorio en `C:\Projects`, ejecutaría:

    cd C:\Projects\ReverseMortgageSimulator

### Crear un entorno virtual

Antes de instalar los paquetes necesarios, se recomienda crear un entorno virtual. Ejecute los siguientes comandos:

#### Windows:

    py -m venv .venv
    .venv\Scripts\activate

#### macOS/Linux:

    python3 -m venv venv
    source venv/bin/activate

### Requisitos de instalación

Una vez activado el entorno virtual, instale los paquetes necesarios mediante el archivo `requirements.txt`:

    pip install -r requirements.txt

### Ejecutar el programa

#### Ejecución de la consola:

Ejecute el archivo `console.py`:

    py src\Console\console.py

#### Ejecución de la GUI:

Si hay una interfaz gráfica de usuario (GUI) disponible, navegue hasta la carpeta `GUI` y ejecute el archivo `gui.py`:

    py src\GUI\gui.py
