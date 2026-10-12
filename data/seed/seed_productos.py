from pymongo import MongoClient
import json

uri = "mongodb+srv://jmezgustavo_db_user:ZnEQC3hj7VEHWSVP@cluster0.qw0lle9.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

db = client["MercadoTico360"]

with open("productos.json", "r", encoding="utf-8") as archivo:
    productos = json.load(archivo)

resultado = db.productos.insert_many(productos)

print(f"Se insertaron {len(resultado.inserted_ids)} productos")