from pymongo import MongoClient
import json


uri = ""

client = MongoClient(uri)

db = client["MercadoTico360"]

clientes = db["clientes"]

with open("clientes.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

resultado = clientes.insert_many(datos)

print(f"Se insertaron {len(resultado.inserted_ids)} clientes")
