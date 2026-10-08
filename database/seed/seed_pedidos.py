from pymongo import MongoClient
import json

uri = ""

client = MongoClient(uri)

db = client["MercadoTico360"]

with open(
    "pedidos.json",
    "r",
    encoding="utf-8"
) as archivo:

    pedidos = json.load(archivo)

resultado = db.pedidos.insert_many(pedidos)

print(
    f"Se insertaron {len(resultado.inserted_ids)} pedidos"
)
