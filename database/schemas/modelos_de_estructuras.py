#Modelos de Estructuras de Datos para MercadoTico 360

from datetime import datetime

#Función para crear un producto
def crear_estructura_producto(
    id_prod: str, #ID del producto, dato tipo texto
    nombre: str, #Nombre del producto, dato tipo texto
    precio: float, #Precio del producto, dato tipo decimal
    categoria: str, #Categoría del producto, dato tipo texto
    comercio_id: str, #ID del comercio del que viene el producto, dato tipo texto
    stock: int, #Stock del producto, dato tipo número entero
    atributos: dict, #Atributos variables del producto
) -> dict:

    #Verifica que campos esenciales no estén vacíos
    if not id_prod or not nombre or precio is None or stock is None:
        raise ValueError("El ID, nombre, precio y stock del producto son obligatorios")

    #Verifica que el precio del producto no sea menor a 0
    if precio < 0:
        raise ValueError("El precio del producto no puede ser menor a 0")

    #Verifica que el stock del producto no sea menor a 0
    if stock < 0:
        raise ValueError("El stock del producto no puede ser menor a 0")

    #Verifica que los atributos únicos del producto sea un diccionario
    if not isinstance(atributos, dict):
        raise ValueError("Los atributos del producto deben ser un diccionario")

    #Diccionario de datos retornados con la información del producto
    return {
        "_id": id_prod,
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria,
        "comercio_id": comercio_id,
        "stock": stock,
        "atributos": atributos,
    }

#Función para crear un comercio
def crear_estructura_comercio(
    id_comercio: str, #ID del comercio, dato tipo texto
    nombre: str, #Nombre del comercio, dato tipo texto
    correo: str, #Correo del comercio, dato tipo texto
    telefono: str, #Teléfono del comercio, dato tipo texto
    categoria: str, #Categoría del comercio, dato tipo texto
    estado: str, #Estado del comercio, dato tipo texto
    provincia: str, #Provincia del comercio, dato tipo texto
    canton: str, #Cantón del comercio, dato tipo texto
    distrito: str, #Distrito del comercio, dato tipo texto
    direccion_exacta: str, #Dirección exacta del comercio, dato tipo texto
) -> dict:

    #Verifica que campos esenciales no estén vacíos
    if not id_comercio or not nombre or not correo or not telefono:
        raise ValueError("El ID, nombre, correo y teléfono del comercio son obligatorios")

    #Verifica que el estado del comercio sea válido
    estados_validos = {"Activo", "Inactivo", "En remodelación"}

    if estado not in estados_validos:
        raise ValueError("El estado del comercio debe ser Activo, Inactivo o En remodelación")

    #Diccionario de datos retornados con la información del comercio
    return {
        "_id": id_comercio,
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "categoria": categoria,
        "estado": estado,
        "direccion": {
            "provincia": provincia,
            "canton": canton,
            "distrito": distrito,
            "direccion_exacta": direccion_exacta,
        },
    }

#Función para crear un cliente
def crear_estructura_cliente(
    id_cliente: str, #ID del cliente, dato tipo texto
    nombre: str, #Nombre del cliente, dato tipo texto
    correo: str, #Correo del cliente, dato tipo texto
    telefono: str, #Teléfono del cliente, dato tipo texto
    cedula: str, #Cédula del cliente, dato tipo texto
    provincia: str, #Provincia del cliente, dato tipo texto
    canton: str, #Cantón del cliente, dato tipo texto
    distrito: str, #Distrito del cliente, dato tipo texto
    direccion_exacta: str, #Dirección exacta del cliente, dato tipo texto
) -> dict:

    #Verifica que campos esenciales no estén vacíos
    if not id_cliente or not nombre or not correo or not cedula or not telefono:
        raise ValueError("El ID, nombre, correo, teléfono y cédula del cliente son obligatorios")

    #Diccionario de datos retornados con la información del cliente
    return {
        "_id": id_cliente,
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "cedula": cedula,
        "direccion": {
            "provincia": provincia,
            "canton": canton,
            "distrito": distrito,
            "direccion_exacta": direccion_exacta,
        },
    }

#Función para crear un pedido
def crear_estructura_pedido(
    id_pedido: str, #ID del pedido, dato tipo texto
    fecha_pedido: datetime, #Fecha y hora del pedido, dato tipo datetime
    cliente_id: str, # ID del cliente que realizó el pedido, dato tipo texto
    estado_pedido: str, #Estado del pedido, dato tipo texto
    lineas_detalle: list, #Lista con los productos incluidos en el pedido
) -> dict:

    #Verifica que campos esenciales no estén vacíos
    if not id_pedido or not fecha_pedido or not cliente_id:
        raise ValueError("El ID, fecha y cliente asociado del pedido son obligatorios")

    #Verifica que el estado del pedido sea válido
    estados_validos = {"Cancelado", "Pendiente", "Enviado", "Entregado"}

    if estado_pedido not in estados_validos:
        raise ValueError(
            "El estado del pedido debe ser Cancelado, Pendiente, Enviado o Entregado")

    #Verifica que el pedido tenga al menos una línea de detalle
    if len(lineas_detalle) == 0:
        raise ValueError("El pedido debe contener al menos un producto")

    #Verifica que la lista con los productos pedidos tenga los campos requeridos
    for linea in lineas_detalle:

        campos_requeridos = {
            "producto_id",
            "nombre_producto",
            "precio_unitario",
            "cantidad",
            "subtotal",
        }

        if not campos_requeridos.issubset(linea):
            raise ValueError("Cada producto del pedido debe contener su ID, nombre, precio por unidad, cantidad pedida y subtotal")

        #Verifica que la cantidad pedida del producto sea mayor que cero
        if linea["cantidad"] <= 0:
            raise ValueError("La cantidad pedida de cada producto debe ser mayor que cero")

        #Verifica que el precio por unidad del producto no sea menor a 0
        if linea["precio_unitario"] < 0:
            raise ValueError("El precio por unidad del producto no puede ser menor a 0")

        #Calcula el subtotal esperado del pedido
        subtotal_esperado = linea["precio_unitario"] * linea["cantidad"]

        #Verifica que el subtotal sea correcto
        if linea["subtotal"] != subtotal_esperado:
            raise ValueError("El subtotal debe ser igual al precio por unidad por la cantidad de unidades pedidas")

    #Calcula el monto total sumando los subtotales de cada producto pedido
    monto_total = sum(
        linea["subtotal"] for linea in lineas_detalle
    )

    #Diccionario de datos retornados con la información del pedido
    return {
        "_id": id_pedido,
        "fecha": fecha_pedido,
        "cliente_id": cliente_id,
        "estado": estado_pedido,
        "monto_total": monto_total,
        "lineas_detalle": lineas_detalle,
    }

#Ejemplo de producto
ejemplo_producto_ropa = crear_estructura_producto(
    id_prod="PROD-001",
    nombre="Camiseta Spiderman",
    precio=18000.00,
    categoria="Ropa",
    comercio_id="COM-102",
    stock=45,
    atributos={
        "talla": "M",
        "color": "Azul",
        "material": "Algodon",
    },
)

#Ejemplo de comercio
ejemplo_comercio = crear_estructura_comercio(
    id_comercio="COM-102",
    nombre="Disfraces Tiquicia",
    correo="contacto@disfracestiquicia.cr",
    telefono="2551-7788",
    categoria="Ropa",
    estado="Activo",
    provincia="Cartago",
    canton="Cartago",
    distrito="Oriental",
    direccion_exacta="100 metros norte del parque central",
)

#Ejemplo de cliente
ejemplo_cliente = crear_estructura_cliente(
    id_cliente="CLI-001",
    nombre="Ariel Rodriguez",
    correo="ariel.rodriguez@gmail.com",
    telefono="8888-1111",
    cedula="102340678",
    provincia="San Jose",
    canton="San Jose",
    distrito="Carmen",
    direccion_exacta="200 metros este de la iglesia",
)

# Ejemplo de líneas de detalle
lineas_ejemplo = [
    {
        "producto_id": "PROD-001",
        "nombre_producto": "Camiseta Spiderman",
        "precio_unitario": 18000.00,
        "cantidad": 2,
        "subtotal": 36000.00,
    }
]

#Ejemplo de pedido
ejemplo_pedido = crear_estructura_pedido(
    id_pedido="PED-001",
    fecha_pedido=datetime(2026, 10, 3, 10, 30),
    cliente_id="CLI-001",
    estado_pedido="Pendiente",
    lineas_detalle=lineas_ejemplo,
)

print(ejemplo_producto_ropa)
print(ejemplo_comercio)
print(ejemplo_cliente)
print(ejemplo_pedido)
