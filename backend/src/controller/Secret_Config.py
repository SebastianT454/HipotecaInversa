"""

Datos secretos que no deben publicarse en el repo

Diligencie estos datos y guarde este archivo como Secret_Config.py
para poder ejecutar la aplicación

"""

import os

PGDATABASE = os.environ.get("PGDATABASE", "postgres-db")
PGUSER = os.environ.get("PGUSER", "root")
PGPASSWORD = os.environ.get("PGPASSWORD", "root")
PGHOST = os.environ.get("PGHOST", "localhost")
PGPORT = int(os.environ.get("PGPORT", "5433"))