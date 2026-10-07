from pymongo import MongoClient
import json


uri = "mongodb+srv://jmezgustavo_db_user:ZnEQC3hj7VEHWSVP@cluster0.qw0lle9.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

db = client["MercadoTico360"]

clientes = db["clientes"]

with open("clientes.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

resultado = clientes.insert_many(datos)

print(f"Se insertaron {len(resultado.inserted_ids)} clientes")