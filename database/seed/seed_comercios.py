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
    "comercios.json"
)

#Carga los comercios desde el archivo JSON
with open(
    ruta_json,
    "r",
    encoding="utf-8"
) as archivo:

    comercios = json.load(archivo)

#Inserta los comercios en MongoDB
resultado = db.comercios.insert_many(
    comercios
)

print(
    f"Se insertaron {len(resultado.inserted_ids)} comercios"
)