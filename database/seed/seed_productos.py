from pymongo import MongoClient
import json

uri = ""

client = MongoClient(uri)

db = client["MercadoTico360"]

with open("productos.json", "r", encoding="utf-8") as archivo:
    productos = json.load(archivo)

resultado = db.productos.insert_many(productos)

print(f"Se insertaron {len(resultado.inserted_ids)} productos")
