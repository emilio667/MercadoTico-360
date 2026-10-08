from pymongo import MongoClient

uri = ""

client = MongoClient(uri)

db = client["MercadoTico360"]

clientes = db["clientes"]

resultado = clientes.insert_one({
    "nombre": "Gustavo Jimenez",
    "correo": "gustavo@test.com",
    "telefono": "88888888"
})

print("Documento creado")
print(resultado.inserted_id)
