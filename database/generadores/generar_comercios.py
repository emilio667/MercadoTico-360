from faker import Faker
from datetime import datetime
from modelos import crear_estructura_comercio
import json

fake = Faker("es_ES")

Faker.seed(67) 
comercios = []

for i in range(200):

    comercio = crear_estructura_comercio(
        id_comercio=f"COM-{i+1:03d}",
        nombre=fake.company(),
        categoria=fake.random_element([
            "Tecnologia",
            "Ropa",
            "Hogar",
            "Deportes",
            "Salud",
            "Belleza",
            "Alimentos",
            "Mascotas"
        ]),
        telefono=fake.numerify("2#######"),
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
    comercio["creado_en"] = datetime.utcnow()
    comercios.append(comercio)

with open("comercios.json", "w", encoding="utf-8") as archivo:
    json.dump(comercios, archivo, ensure_ascii=False, indent=4,default=str)

print(f"Se generaron {len(comercios)} comercios")
