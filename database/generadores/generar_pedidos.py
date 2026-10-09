from pymongo import MongoClient
from modelos import crear_estructura_pedido
from faker import Faker
from datetime import datetime
import random
import json

fake = Faker("es_ES")
Faker.seed(42)
uri = ""   #aqui hay que poner el uri de cada 1

client = MongoClient(uri)

db = client["MercadoTico360"]

clientes = list(
    db.clientes.find(
        {},
        {"_id": 1}
    )
)

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

pedidos = []

for i in range(50000):

    cliente = random.choice(clientes)

    cantidad_lineas = random.randint(1, 5)

    lineas = []

    for _ in range(cantidad_lineas):

        producto = random.choice(productos)

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
	fecha=str(fake.date_this_year()),
	cliente_id=str(cliente["_id"]),
	estado=random.choice([
            "Pendiente",
            "Enviado",
            "Entregado",
            "Cancelado"
        ]),
        lineas_detalle=lineas
    )

    pedidos.append(pedido)

with open(
    "pedidos.json",
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        pedidos,
        archivo,
        ensure_ascii=False,
        indent=4
    )

print(
    f"Se generaron {len(pedidos)} pedidos"
)
