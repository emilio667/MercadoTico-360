from pymongo import MongoClient
from dotenv import load_dotenv
import os
import json

#Carga las variables del archivo .env
load_dotenv()

#Obtiene la URI de conexión
uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError(
        "No se encontró MONGODB_URI en el archivo .env"
    )

#Obtiene el nombre de la base de datos
nombre_db = os.getenv("MONGODB_DB")

if not nombre_db:
    raise ValueError(
        "No se encontró MONGODB_DB en el archivo .env"
    )

#Conexión con MongoDB
client = MongoClient(uri)

#Base de datos utilizada
db = client[nombre_db]

ruta_actual = os.path.dirname(__file__)

ruta_json = os.path.join(
    ruta_actual,
    "productos.json"
)

#Carga los productos desde el archivo JSON
with open(
    ruta_json,
    "r",
    encoding="utf-8"
) as archivo:

    productos = json.load(archivo)

#Inserta los productos en MongoDB
resultado = db.productos.insert_many(
    productos
)

print(
    f"Se insertaron {len(resultado.inserted_ids)} productos"
)