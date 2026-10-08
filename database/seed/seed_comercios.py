from pymongo import MongoClient
import json

uri = ""

client = MongoClient(uri)

db = client["MercadoTico360"]

with open("comercios.json", "r", encoding="utf-8") as archivo:
    comercios = json.load(archivo)

resultado = db.comercios.insert_many(comercios)

print(f"Se insertaron {len(resultado.inserted_ids)} comercios")
