#Operaciones CRUD para MercadoTico 360

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

#Colecciones permitidas
colecciones_validas = {
    "productos",
    "comercios",
    "clientes",
    "pedidos",
}

#Función para crear un documento
def crear_documento(nombre_coleccion: str, documento: dict):

    if nombre_coleccion not in colecciones_validas:
        raise ValueError("La colección indicada no es válida")

    if not isinstance(documento, dict):
        raise ValueError("El documento debe ser un diccionario")

    coleccion = db[nombre_coleccion]

    resultado = coleccion.insert_one(documento)

    return resultado.inserted_id

#Función para buscar un documento por su ID
def buscar_documento(nombre_coleccion: str, id_documento: str):

    if nombre_coleccion not in colecciones_validas:
        raise ValueError("La colección indicada no es válida")

    if not id_documento:
        raise ValueError("El ID del documento es obligatorio")

    coleccion = db[nombre_coleccion]

    documento = coleccion.find_one({
        "_id": id_documento
    })

    return documento

#Función para buscar varios documentos
def buscar_documentos(nombre_coleccion: str, filtro: dict = None):

    if nombre_coleccion not in colecciones_validas:
        raise ValueError("La colección indicada no es válida")

    coleccion = db[nombre_coleccion]

    if filtro is None:
        filtro = {}

    resultados = coleccion.find(filtro)

    return list(resultados)

#Función para actualizar un documento por su ID
def actualizar_documento(
    nombre_coleccion: str,
    id_documento: str,
    datos_actualizados: dict,
):

    if nombre_coleccion not in colecciones_validas:
        raise ValueError("La colección indicada no es válida")

    if not id_documento:
        raise ValueError("El ID del documento es obligatorio")

    if not isinstance(datos_actualizados, dict):
        raise ValueError("Los datos actualizados deben ser un diccionario")

    if "_id" in datos_actualizados:
        raise ValueError("El identificador _id no puede ser modificado")

    coleccion = db[nombre_coleccion]

    resultado = coleccion.update_one(
        {
            "_id": id_documento
        },
        {
            "$set": datos_actualizados
        }
    )

    return resultado.modified_count

#Función para eliminar un documento por su ID
def eliminar_documento(nombre_coleccion: str, id_documento: str):

    if nombre_coleccion not in colecciones_validas:
        raise ValueError("La colección indicada no es válida")

    if not id_documento:
        raise ValueError("El ID del documento es obligatorio")

    coleccion = db[nombre_coleccion]

    resultado = coleccion.delete_one({
        "_id": id_documento
    })

    return resultado.deleted_count

#Función para verificar si un documento existe
def existe_documento(nombre_coleccion: str, id_documento: str):

    if nombre_coleccion not in colecciones_validas:
        raise ValueError("La colección indicada no es válida")

    if not id_documento:
        raise ValueError("El ID del documento es obligatorio")

    coleccion = db[nombre_coleccion]

    documento = coleccion.find_one({
        "_id": id_documento
    })

    return documento is not None

#Función para contar documentos de una colección
def contar_documentos(nombre_coleccion: str, filtro: dict = None):

    if nombre_coleccion not in colecciones_validas:
        raise ValueError("La colección indicada no es válida")

    coleccion = db[nombre_coleccion]

    if filtro is None:
        filtro = {}

    cantidad = coleccion.count_documents(filtro)

    return cantidad

#Función para crear un producto
def crear_producto(producto: dict):

    return crear_documento(
        "productos",
        producto
    )

#Función para buscar un producto
def buscar_producto(id_producto: str):

    return buscar_documento(
        "productos",
        id_producto
    )

#Función para actualizar un producto
def actualizar_producto(
    id_producto: str,
    datos_actualizados: dict,
):

    return actualizar_documento(
        "productos",
        id_producto,
        datos_actualizados
    )

#Función para eliminar un producto
def eliminar_producto(id_producto: str):

    return eliminar_documento(
        "productos",
        id_producto
    )

#Función para crear un comercio
def crear_comercio(comercio: dict):

    return crear_documento(
        "comercios",
        comercio
    )

#Función para buscar un comercio
def buscar_comercio(id_comercio: str):

    return buscar_documento(
        "comercios",
        id_comercio
    )

#Función para actualizar un comercio
def actualizar_comercio(
    id_comercio: str,
    datos_actualizados: dict,
):

    return actualizar_documento(
        "comercios",
        id_comercio,
        datos_actualizados
    )

#Función para eliminar un comercio
def eliminar_comercio(id_comercio: str):

    return eliminar_documento(
        "comercios",
        id_comercio
    )

#Función para crear un cliente
def crear_cliente(cliente: dict):

    return crear_documento(
        "clientes",
        cliente
    )

#Función para buscar un cliente
def buscar_cliente(id_cliente: str):

    return buscar_documento(
        "clientes",
        id_cliente
    )

#Función para actualizar un cliente
def actualizar_cliente(
    id_cliente: str,
    datos_actualizados: dict,
):

    return actualizar_documento(
        "clientes",
        id_cliente,
        datos_actualizados
    )

#Función para eliminar un cliente
def eliminar_cliente(id_cliente: str):

    return eliminar_documento(
        "clientes",
        id_cliente
    )

#Función para crear un pedido
def crear_pedido(pedido: dict):

    return crear_documento(
        "pedidos",
        pedido
    )

#Función para buscar un pedido
def buscar_pedido(id_pedido: str):

    return buscar_documento(
        "pedidos",
        id_pedido
    )

#Función para actualizar un pedido
def actualizar_pedido(
    id_pedido: str,
    datos_actualizados: dict,
):

    return actualizar_documento(
        "pedidos",
        id_pedido,
        datos_actualizados
    )

#Función para eliminar un pedido
def eliminar_pedido(id_pedido: str):

    return eliminar_documento(
        "pedidos",
        id_pedido
    )

