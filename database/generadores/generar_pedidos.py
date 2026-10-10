#Generador de pedidos para MercadoTico 360

import os
import random
import json

from faker import Faker
from dotenv import load_dotenv
from pymongo import MongoClient

from database.schemas.modelos_de_estructuras import crear_estructura_pedido

Faker.seed(123)
fake = Faker("es_ES")

#Carga las variables del archivo .env
load_dotenv()

#Obtiene la URI de conexión
uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("No se encontró MONGODB_URI en el archivo .env")

#Obtiene el nombre de la base de datos
nombre_db = os.getenv("MONGODB_DB")

if not nombre_db:
    raise ValueError("No se encontró MONGODB_DB en el archivo .env")

#Conexión con MongoDB Atlas
client = MongoClient(uri)

#Base de datos utilizada
db = client[nombre_db]

#Obtiene los IDs de los clientes existentes
clientes = list(
    db.clientes.find(
        {},
        {
            "_id": 1
        }
    )
)

#Obtiene la información necesaria de los productos existentes
productos = list(
    db.productos.find(
        {},
        {
            "_id": 1,
            "nombre": 1,
            "precio": 1
        }
    )
)

#Verifica que existan clientes y productos antes de generar pedidos
if len(clientes) == 0:
    raise ValueError(
        "No existen clientes en la base de datos"
    )

if len(productos) == 0:
    raise ValueError(
        "No existen productos en la base de datos"
    )

pedidos = []

for i in range(50000):

    cliente = random.choice(clientes)

    #Cantidad de productos diferentes dentro del pedido
    cantidad_lineas = random.randint(2, 5)

    #Evita repetir el mismo producto dentro del mismo pedido
    productos_pedido = random.sample(
        productos,
        cantidad_lineas
    )

    lineas = []

    for producto in productos_pedido:

        cantidad = random.randint(1, 3)

        subtotal = producto["precio"] * cantidad

        lineas.append({
            "producto_id": producto["_id"],
            "nombre_producto": producto["nombre"],
            "precio_unitario": producto["precio"],
            "cantidad": cantidad,
            "subtotal": subtotal
        })

    pedido = crear_estructura_pedido(
        id_pedido=f"PED-{i+1:05d}",
        fecha_pedido=fake.date_time_this_year(),
        cliente_id=cliente["_id"],
        estado_pedido=random.choice([
            "Pendiente",
            "Enviado",
            "Entregado",
            "Cancelado"
        ]),
        lineas_detalle=lineas
    )

    pedidos.append(pedido)

ruta_actual = os.path.dirname(__file__)

ruta_json = os.path.join(
    ruta_actual,
    "pedidos.json"
)

with open(
    ruta_json,
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        pedidos,
        archivo,
        ensure_ascii=False,
        indent=4,
        default=str
    )

print(
    f"Se generaron {len(pedidos)} pedidos"
)
