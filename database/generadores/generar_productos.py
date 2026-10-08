from faker import Faker
from modelos import crear_estructura_producto
import random
import json

fake = Faker("es_ES")

categorias = [
    "Tecnologia",
    "Ropa",
    "Hogar",
    "Deportes",
    "Salud",
    "Belleza",
    "Alimentos",
    "Mascotas"
]

productos = []

for i in range(25000):

    categoria = random.choice(categorias)

    producto = crear_estructura_producto(
        id_prod=f"PROD-{i+1:05d}",
        nombre=fake.word().capitalize(),
        precio=round(random.uniform(1000, 500000), 2),
        categoria=categoria,
        comercio_id=f"COM-{random.randint(1,100):03d}",
        stock=random.randint(0, 500),
        atributos={
            "marca": fake.company()
        }
    )

    productos.append(producto)

with open("productos.json", "w", encoding="utf-8") as archivo:
    json.dump(productos, archivo, ensure_ascii=False, indent=4)

print(f"Se generaron {len(productos)} productos")