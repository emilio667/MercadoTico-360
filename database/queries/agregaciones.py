#Consultas de agregación para MercadoTico 360

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

#Colecciones utilizadas
pedidos = db["pedidos"]
productos = db["productos"]


#Función para calcular el total de ventas por categoría
def ventas_por_categoria():

    pipeline = [
        {
            "$match": {
                "estado": {
                    "$ne": "Cancelado"
                }
            }
        },
        {
            "$unwind": "$lineas_detalle"
        },
        {
            "$lookup": {
                "from": "productos",
                "localField": "lineas_detalle.producto_id",
                "foreignField": "_id",
                "as": "producto"
            }
        },
        {
            "$unwind": "$producto"
        },
        {
            "$group": {
                "_id": "$producto.categoria",
                "total_ventas": {
                    "$sum": "$lineas_detalle.subtotal"
                }
            }
        },
        {
            "$sort": {
                "total_ventas": -1
            }
        }
    ]

    resultados = pedidos.aggregate(pipeline)

    return list(resultados)


#Función para obtener los productos más vendidos
def productos_mas_vendidos():

    pipeline = [
        {
            "$match": {
                "estado": {
                    "$ne": "Cancelado"
                }
            }
        },
        {
            "$unwind": "$lineas_detalle"
        },
        {
            "$group": {
                "_id": "$lineas_detalle.producto_id",
                "nombre_producto": {
                    "$first": "$lineas_detalle.nombre_producto"
                },
                "cantidad_vendida": {
                    "$sum": "$lineas_detalle.cantidad"
                }
            }
        },
        {
            "$sort": {
                "cantidad_vendida": -1
            }
        },
        {
            "$limit": 10
        }
    ]

    resultados = pedidos.aggregate(pipeline)

    return list(resultados)


#Función para calcular el ticket promedio de los pedidos
def ticket_promedio():

    pipeline = [
        {
            "$match": {
                "estado": {
                    "$ne": "Cancelado"
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "ticket_promedio": {
                    "$avg": "$monto_total"
                },
                "cantidad_pedidos": {
                    "$sum": 1
                }
            }
        }
    ]

    resultados = pedidos.aggregate(pipeline)

    return list(resultados)


#Función para calcular ventas por estado del pedido
def ventas_por_estado():

    pipeline = [
        {
            "$group": {
                "_id": "$estado",
                "cantidad_pedidos": {
                    "$sum": 1
                },
                "monto_total": {
                    "$sum": "$monto_total"
                }
            }
        },
        {
            "$sort": {
                "monto_total": -1
            }
        }
    ]

    resultados = pedidos.aggregate(pipeline)

    return list(resultados)


#Función para obtener pedidos completos con información del cliente
def pedidos_con_cliente():

    pipeline = [
        {
            "$lookup": {
                "from": "clientes",
                "localField": "cliente_id",
                "foreignField": "_id",
                "as": "cliente"
            }
        },
        {
            "$unwind": "$cliente"
        },
        {
            "$project": {
                "_id": 1,
                "fecha": 1,
                "estado": 1,
                "monto_total": 1,
                "lineas_detalle": 1,
                "cliente._id": 1,
                "cliente.nombre": 1,
                "cliente.correo": 1
            }
        }
    ]

    resultados = pedidos.aggregate(pipeline)

    return list(resultados)


#Función para obtener ventas de una categoría específica
def ventas_categoria_especifica(categoria: str):

    pipeline = [
        {
            "$match": {
                "estado": {
                    "$ne": "Cancelado"
                }
            }
        },
        {
            "$unwind": "$lineas_detalle"
        },
        {
            "$lookup": {
                "from": "productos",
                "localField": "lineas_detalle.producto_id",
                "foreignField": "_id",
                "as": "producto"
            }
        },
        {
            "$unwind": "$producto"
        },
        {
            "$match": {
                "producto.categoria": categoria
            }
        },
        {
            "$group": {
                "_id": "$producto.categoria",
                "total_ventas": {
                    "$sum": "$lineas_detalle.subtotal"
                },
                "cantidad_unidades": {
                    "$sum": "$lineas_detalle.cantidad"
                }
            }
        }
    ]

    resultados = pedidos.aggregate(pipeline)

    return list(resultados)