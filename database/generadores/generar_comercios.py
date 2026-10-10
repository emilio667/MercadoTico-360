#Generador de comercios para MercadoTico 360

from faker import Faker
import json
import os

from database.schemas.modelos_de_estructuras import crear_estructura_comercio

fake = Faker("es_ES")

categorias = [
    "Alimentos",
    "Ropa",
    "Tecnología",
    "Artesanías",
    "Servicios",
    "Hogar",
    "Belleza",
    "Deportes"
]

estados = [
    "Activo",
    "Inactivo",
    "En remodelación"
]

provincias = [
    "San José",
    "Alajuela",
    "Cartago",
    "Heredia",
    "Guanacaste",
    "Puntarenas",
    "Limón"
]

comercios = []

for i in range(500):

    comercio = crear_estructura_comercio(
        id_comercio=f"COM-{i+1:03d}",
        nombre=fake.company(),
        correo=fake.company_email(),
        telefono=fake.numerify("2#######"),
        categoria=fake.random_element(categorias),
        estado=fake.random_element(estados),
        provincia=fake.random_element(provincias),
        canton=fake.city(),
        distrito=fake.city(),
        direccion_exacta=fake.street_address()
    )

    comercios.append(comercio)

ruta_actual = os.path.dirname(__file__)

ruta_json = os.path.join(
    ruta_actual,
    "comercios.json"
)

with open(
    ruta_json,
    "w",
    encoding="utf-8"
) as archivo:

    json.dump(
        comercios,
        archivo,
        ensure_ascii=False,
        indent=4
    )

print(
    f"Se generaron {len(comercios)} comercios"
)