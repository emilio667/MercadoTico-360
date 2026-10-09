#Generador de productos para MercadoTico 360

from faker import Faker
import random
import json
import os

from database.schemas.modelos_de_estructuras import crear_estructura_producto

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

atributos_por_categoria = {
    "Alimentos": {
        "peso_gramos": [250, 500, 750, 1000],
        "origen": ["Costa Rica", "Importado"],
        "organico": [True, False],
        "tipo": ["Natural", "Procesado"]
    },

    "Ropa": {
        "talla": ["XS", "S", "M", "L", "XL"],
        "color": ["Negro", "Blanco", "Azul", "Rojo", "Verde"],
        "material": ["Algodón", "Poliéster", "Lino"],
        "genero": ["Hombre", "Mujer", "Unisex"]
    },

    "Tecnología": {
        "marca": ["Samsung", "Apple", "Xiaomi", "Logitech", "Sony"],
        "garantia_meses": [6, 12, 24],
        "almacenamiento": ["64 GB", "128 GB", "256 GB", "512 GB"],
        "inalambrico": [True, False]
    },

    "Artesanías": {
        "material": ["Madera", "Cerámica", "Cuero", "Tela"],
        "tecnica": ["Tallado", "Pintado a mano", "Tejido"],
        "origen": ["Cartago", "Guanacaste", "Limón", "San José"],
        "hecho_a_mano": [True, False]
    },

    "Servicios": {
        "duracion_minutos": [30, 60, 90, 120],
        "modalidad": ["Presencial", "Virtual"],
        "requiere_cita": [True, False],
        "cobertura": ["Local", "Nacional", "Virtual"]
    },

    "Hogar": {
        "material": ["Madera", "Metal", "Plástico", "Vidrio"],
        "color": ["Blanco", "Negro", "Gris", "Café"],
        "requiere_armado": [True, False],
        "uso": ["Interior", "Exterior"]
    },

    "Belleza": {
        "marca": ["Natural CR", "Belleza Tica", "Pura Vida"],
        "tipo_piel": ["Seca", "Grasa", "Mixta", "Todo tipo"],
        "contenido_ml": [50, 100, 250, 500],
        "vegano": [True, False]
    },

    "Deportes": {
        "deporte": ["Fútbol", "Ciclismo", "Running", "Natación"],
        "talla": ["S", "M", "L"],
        "material": ["Poliéster", "Caucho", "Metal"],
        "uso": ["Entrenamiento", "Competencia", "Recreativo"]
    }
}

#Función para generar atributos variables según la categoría
def generar_atributos(categoria):

    atributos_posibles = atributos_por_categoria[categoria]

    cantidad_atributos = random.randint(
        2,
        len(atributos_posibles)
    )

    campos_elegidos = random.sample(
        list(atributos_posibles.keys()),
        cantidad_atributos
    )

    atributos = {}

    for campo in campos_elegidos:
        atributos[campo] = random.choice(
            atributos_posibles[campo]
        )

    return atributos

productos = []

for i in range(25000):

    categoria = random.choice(categorias)

    producto = crear_estructura_producto(
        id_prod=f"PROD-{i+1:05d}",
        nombre=fake.word().capitalize(),
        precio=round(random.uniform(1000, 500000), 2),
        categoria=categoria,
        comercio_id=f"COM-{random.randint(1,500):03d}",
        stock=random.randint(0, 500),
        atributos=generar_atributos(categoria)
    )

    productos.append(producto)

ruta_actual = os.path.dirname(__file__)

ruta_json = os.path.join(
    ruta_actual,
    "productos.json"
)

with open(ruta_json, "w", encoding="utf-8") as archivo:
    json.dump(
        productos,
        archivo,
        ensure_ascii=False,
        indent=4
    )

print(f"Se generaron {len(productos)} productos")