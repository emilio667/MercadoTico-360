#  Modelos de Estructuras de Datos para MercadoTico 360

# Función para crear un producto
def crear_estructura_producto(  # funcion para crear la estructura del producto
    id_prod: str,           # dato tipo texto
    nombre: str,
    precio: float,          # dato tipo decimal
    categoria: str,
    comercio_id: str,
    stock: int,            # dato tipo numero entero
    atributos: dict,       # diccionario 
) -> dict:                     # la función retorna el diccionario con la estructura oficial para un producto del catalogo

    return {                       #entrega el resultado final del diccionario
        "_id":id_prod,
        "nombre":nombre,
        "precio":precio,
        "categoria":categoria,
        "comercio_id":comercio_id,
        "stock":stock,
        "atributos":atributos,
    } 

# Funcion para crear un pedido
def crear_estructura_pedido(
    id_pedido: str,
    fecha: str,
    cliente_id: str,
    estado: str,
    lineas_detalle: list[dict],  # este parametro debe ser una lista llena de diccionarios (una lista de líneas de compra con producto, cantidad y precio)
) -> dict:
    monto_total = sum(
        item["subtotal"] for item in lineas_detalle # calcula el total del pedido
    )
    return {
        "_id": id_pedido,
        "fecha": fecha,
        "cliente_id": cliente_id,
        "estado": estado,
        "monto_total": monto_total,
        "lineas_detalle": lineas_detalle,
    }

# ejemplo con datos 
ejemplo_producto_ropa = crear_estructura_producto(
    id_prod="PROD-001",
    nombre="Camiseta Tipica",
    precio=18000.00,
    categoria="Ropa",
    comercio_id="COM-102",
    stock=45,
    atributos={"talla": "M", "color": "Azul", "material": "Algodon"},
)

print(ejemplo_producto_ropa)
