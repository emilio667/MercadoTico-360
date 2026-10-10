#Generador de clientes para MercadoTico 360

from faker import Faker
import json
import os

from database.schemas.modelos_de_estructuras import crear_estructura_cliente
Faker.seed(123)
fake = Faker("es_ES")

provincias = [
    "San José",
    "Alajuela",
    "Cartago",
    "Heredia",
    "Guanacaste",
    "Puntarenas",
    "Limón"
]

clientes = []

for i in range(10000):

    cliente = crear_estructura_cliente(
        id_cliente=f"CLI-{i+1:05d}",
        nombre=fake.name(),
        correo=fake.email(),
        telefono=fake.numerify("8#######"),
        cedula=f"{fake.random_int(1,9)}-{fake.random_int(1000,9999)}-{fake.random_int(1000,9999)}",
        provincia=fake.random_element(provincias),
        canton=fake.city(),
        distrito=fake.city(),
        direccion_exacta=fake.street_address()
    )

    clientes.append(cliente)

ruta_actual = os.path.dirname(__file__)

ruta_json = os.path.join(
    ruta_actual,
    "clientes.json"
)

with open(
    ruta_json,
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        clientes,
        archivo,
        ensure_ascii=False,
        indent=4
    )

print(
    f"Se generaron {len(clientes)} clientes"
)
