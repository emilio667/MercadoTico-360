from faker import Faker
from modelos import crear_estructura_producto
import random
import json

fake = Faker("es_ES")
Faker.seed(67)

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

    categoria = fake.random_element(categorias)

    nombre_producto = fake.catch_phrase().split(" y ")[0].capitalize()
    
    producto = crear_estructura_producto(
        id_prod=f"PROD-{i+1:05d}",
        nombre=nombre_producto,
        precio=round(random.uniform(1000, 500000), 2),#precio=float(fake.random_int(min=1000, max=500000)),
        categoria=categoria,
        comercio_id=f"COM-{fake.random_int(min=1, max=200):03d}",
        stock=fake.random_int(min=0, max=500),
        atributos={
            "marca": fake.company(),
           
            "especificaciones": {
                "color": fake.color_name(),
                "origen": fake.country()
        }
    )
    producto["actualizado_en"] = datetime.utcnow()
    productos.append(producto)

with open("productos.json", "w", encoding="utf-8") as archivo:
    json.dump(productos, archivo, ensure_ascii=False, indent=4,default=str)

print(f"Se generaron {len(productos)} productos exitosamente.")
