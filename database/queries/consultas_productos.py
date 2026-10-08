#Consultas de productos para MercadoTico 360

import os
from dotenv import load_dotenv
from pymongo import MongoClient

#Carga las variables del archivo .env
load_dotenv()

#Obtiene la URI de conexión
uri = os.getenv("MONGODB_URI")

if not uri:
    raise ValueError("No se encontró MONGODB_URI en el archivo .env")

#Conexión con MongoDB Atlas
client = MongoClient(uri)

#Base de datos utilizada
db = client["MercadoTico360"]

#Colección de productos
productos = db["productos"]

#Categorías permitidas
categorias_validas = {
    "Alimentos",
    "Ropa",
    "Tecnología",
    "Artesanías",
    "Servicios",
    "Hogar",
    "Belleza",
    "Deportes",
}

#Función para buscar productos por categoría
def buscar_por_categoria(categoria: str):

    if categoria not in categorias_validas:
        raise ValueError("La categoría indicada no es válida")

    resultados = productos.find({
        "categoria": categoria
    })

    return list(resultados)

#Función para buscar productos por rango de precio
def buscar_por_rango_precio(
    precio_minimo: float,
    precio_maximo: float,
):

    if precio_minimo < 0 or precio_maximo < 0:
        raise ValueError("Los precios no pueden ser menores a 0")

    if precio_minimo > precio_maximo:
        raise ValueError("El precio mínimo no puede ser mayor que el precio máximo")

    resultados = productos.find({
        "precio": {
            "$gte": precio_minimo,
            "$lte": precio_maximo
        }
    })

    return list(resultados)

#Función para buscar productos por un atributo específico
def buscar_por_atributo(
    nombre_atributo: str,
    valor_atributo,
):

    if not nombre_atributo:
        raise ValueError("El nombre del atributo es obligatorio")

    campo = f"atributos.{nombre_atributo}"

    resultados = productos.find({
        campo: valor_atributo
    })

    return list(resultados)

#Función para buscar productos por categoría y rango de precio
def buscar_por_categoria_y_precio(
    categoria: str,
    precio_minimo: float,
    precio_maximo: float,
):

    if categoria not in categorias_validas:
        raise ValueError("La categoría indicada no es válida")

    if precio_minimo < 0 or precio_maximo < 0:
        raise ValueError("Los precios no pueden ser menores a 0")

    if precio_minimo > precio_maximo:
        raise ValueError("El precio mínimo no puede ser mayor que el precio máximo")

    resultados = productos.find({
        "categoria": categoria,
        "precio": {
            "$gte": precio_minimo,
            "$lte": precio_maximo
        }
    })

    return list(resultados)

#Función para buscar productos por categoría y atributo específico
def buscar_por_categoria_y_atributo(
    categoria: str,
    nombre_atributo: str,
    valor_atributo,
):

    if categoria not in categorias_validas:
        raise ValueError("La categoría indicada no es válida")

    if not nombre_atributo:
        raise ValueError("El nombre del atributo es obligatorio")

    campo = f"atributos.{nombre_atributo}"

    resultados = productos.find({
        "categoria": categoria,
        campo: valor_atributo
    })

    return list(resultados)


#Función para buscar productos disponibles en stock
def buscar_productos_disponibles():

    resultados = productos.find({
        "stock": {
            "$gt": 0
        }
    })

    return list(resultados)


#Función para buscar productos de un comercio
def buscar_productos_por_comercio(comercio_id: str):

    if not comercio_id:
        raise ValueError("El ID del comercio es obligatorio")

    resultados = productos.find({
        "comercio_id": comercio_id
    })

    return list(resultados)