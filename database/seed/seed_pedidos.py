from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
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
    "pedidos.json"
)

#Carga los pedidos desde el archivo JSON
with open(
    ruta_json,
    "r",
    encoding="utf-8"
) as archivo:

    pedidos = json.load(archivo)

#Convierte la fecha de texto a datetime
for pedido in pedidos:

    pedido["fecha"] = datetime.fromisoformat(
        pedido["fecha"]
    )

#Inserta los pedidos en MongoDB
resultado = db.pedidos.insert_many(
    pedidos
)

print(
    f"Se insertaron {len(resultado.inserted_ids)} pedidos"
)