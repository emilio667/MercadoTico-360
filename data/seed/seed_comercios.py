from pymongo import MongoClient
import json

uri = "mongodb+srv://jmezgustavo_db_user:ZnEQC3hj7VEHWSVP@cluster0.qw0lle9.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

db = client["MercadoTico360"]

with open("comercios.json", "r", encoding="utf-8") as archivo:
    comercios = json.load(archivo)

resultado = db.comercios.insert_many(comercios)

print(f"Se insertaron {len(resultado.inserted_ids)} comercios")