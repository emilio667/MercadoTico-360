#Consultas de pedidos para MercadoTico 360

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

#Colección de pedidos
pedidos = db["pedidos"]

#Estados permitidos
estados_validos = {
    "Cancelado",
    "Pendiente",
    "Enviado",
    "Entregado",
}


#Función para buscar un pedido por su ID
def buscar_pedido_por_id(id_pedido: str):

    if not id_pedido:
        raise ValueError("El ID del pedido es obligatorio")

    pedido = pedidos.find_one({
        "_id": id_pedido
    })

    return pedido


#Función para buscar todos los pedidos de un cliente
def buscar_pedidos_por_cliente(cliente_id: str):

    if not cliente_id:
        raise ValueError("El ID del cliente es obligatorio")

    resultados = pedidos.find({
        "cliente_id": cliente_id
    })

    return list(resultados)


#Función para buscar pedidos de un cliente ordenados por fecha
def buscar_pedidos_cliente_por_fecha(cliente_id: str):

    if not cliente_id:
        raise ValueError("El ID del cliente es obligatorio")

    resultados = pedidos.find({
        "cliente_id": cliente_id
    }).sort(
        "fecha",
        -1
    )

    return list(resultados)


#Función para buscar pedidos por estado
def buscar_pedidos_por_estado(estado: str):

    if estado not in estados_validos:
        raise ValueError("El estado debe ser Cancelado, Pendiente, Enviado o Entregado")

    resultados = pedidos.find({
        "estado": estado
    })

    return list(resultados)


#Función para buscar pedidos de un cliente por estado
def buscar_pedidos_cliente_por_estado(
    cliente_id: str,
    estado: str,
):

    if not cliente_id:
        raise ValueError("El ID del cliente es obligatorio")

    if estado not in estados_validos:
        raise ValueError("El estado debe ser Cancelado, Pendiente, Enviado o Entregado")

    resultados = pedidos.find({
        "cliente_id": cliente_id,
        "estado": estado
    })

    return list(resultados)


#Función para actualizar el estado de un pedido
def actualizar_estado_pedido(
    id_pedido: str,
    nuevo_estado: str,
):

    if not id_pedido:
        raise ValueError("El ID del pedido es obligatorio")

    if nuevo_estado not in estados_validos:
        raise ValueError("El estado debe ser Cancelado, Pendiente, Enviado o Entregado")

    resultado = pedidos.update_one(
        {
            "_id": id_pedido
        },
        {
            "$set": {
                "estado": nuevo_estado
            }
        }
    )

    return resultado.modified_count


#Función para buscar pedidos que contengan un producto específico
def buscar_pedidos_por_producto(producto_id: str):

    if not producto_id:
        raise ValueError("El ID del producto es obligatorio")

    resultados = pedidos.find({
        "lineas_detalle.producto_id": producto_id
    })

    return list(resultados)


#Función para contar los pedidos de un cliente
def contar_pedidos_cliente(cliente_id: str):

    if not cliente_id:
        raise ValueError("El ID del cliente es obligatorio")

    cantidad = pedidos.count_documents({
        "cliente_id": cliente_id
    })

    return cantidad