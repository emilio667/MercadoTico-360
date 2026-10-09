from faker import Faker
from datetime import datetime #tipo datetime
from modelos import crear_estructura_cliente
import json

fake = Faker("es_ES")
Faker.seed(67)
clientes = []

for i in range(10000):

    cliente = crear_estructura_cliente(
        id_cliente=f"CLI-{i+1:05d}",
        nombre=fake.name(),
        correo=fake.email(),
        telefono=fake.numerify("8#######"),
        cedula=f"{fake.random_int(1,9)}-{fake.random_int(1000,9999)}-{fake.random_int(1000,9999)}",
        direccion={
            "provincia": fake.random_element([
                "San José",
                "Alajuela",
                "Cartago",
                "Heredia",
                "Guanacaste",
                "Puntarenas",
                "Limón"
            ]),
            "canton": fake.city(),
            "distrito": fake.city(),
            "direccion_exacta": fake.street_address()
        }
    )
    cliente["creado_en"] = datetime.utcnow() #Se rearon marcas de fechas a los datos
    clientes.append(cliente)

with open("clientes.json", "w", encoding="utf-8") as archivo:
    json.dump(clientes, archivo, ensure_ascii=False, indent=4, default=str)

print(f"Se generaron {len(clientes)} clientes")
