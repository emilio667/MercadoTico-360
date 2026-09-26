#  Modelos de Estructuras de Datos para MercadoTico 360

# 1. FUNCIÓN PARA CREAR UN PRODUCTO
def crear_estructura_producto(  # funcion para crear la estructura del producto
    id_prod: str,           # dato tipo texto
    nombre: str,
    precio: float,          # dato tipo decimal
    categoria: str,
    comercio_id: str,
    stock: int,            # dato tipo numero entero
    atributos: dict,       # diccionario: objeto embebido que contiene un conjunto de clave-valor que varía segun la categoria
) -> dict:                     # la función retorna el diccionario con la estructura oficial para un producto del catalogo
    """Retorna la estructura oficial para un producto del catálogo heterogéneo."""
    return {                       #entrega el resultado final del diccionario
        "_id":id_prod,
        "nombre":nombre,
        "precio":precio,
        "categoria":categoria,
        "comercio_id":comercio_id,
        "stock":stock,
        "atributos":atributos,
    } 

# 2. FUNCIÓN PARA CREAR LA ESTRUCTURA DE UN CLIENTES
def crear_estructura_cliente(
    id_cliente: str,  
    nombre: str,
    correo: str,
    telefono: str,
    cedula: str,
    direccion: dict,  # objeto embebido con provincia, canton, distrito, etc.
) -> dict:  # la función retorna el diccionario con la estructura oficial del cliente
    """Retorna la estructura oficial para un cliente con su dirección embebida."""
    return {
        "_id": id_cliente,
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "cedula": cedula,
        "direccion": direccion,  # dirección estructurada como objeto embebido
    }


# FUNCIÓN PARA CREAR UN PEDIDO
def crear_estructura_pedido(
    id_pedido: str,
    fecha: str,
    cliente_id: str,
    estado: str,
    lineas_detalle: list[dict],  # lista: arreglo de objetos embebidos, contiene multiples objetos, uno por cada producto diferente que compro el cliente
) -> dict:                      # la función retorna el diccionario con la estructura oficial del pedido
    """Retorna la estructura de un pedido con sus líneas de detalle embebidas."""
    monto_total = sum(item["subtotal"] for item in lineas_detalle) # calcula el total del pedido)
    return {
        "_id": id_pedido,
        "fecha": fecha,
        "cliente_id": cliente_id,
        "estado": estado,
        "monto_total": monto_total,
        "lineas_detalle": lineas_detalle,
    }




# ==========================================
# EJEMPLOS DE PRUEBA LOCAL
# ==========================================
if __name__ == "__main__":
    prod_prueba = crear_estructura_producto(
        id_prod="PROD-001",
        nombre="Camiseta Típica",
        precio=18000.00,
        categoria="Ropa",
        comercio_id="COM-102",
        stock=45,
        atributos={"talla": "M", "color": "Azul", "material": "Algodón"},
    )

    cliente_prueba = crear_estructura_cliente(
        id_cliente="CLI-1001",
        nombre="María Rodríguez",
        correo="maria.rodriguez@email.com",
        telefono="8888-5555",
        cedula="1-1234-0567",
        direccion={
            "provincia": "San José",
            "canton": "Montes de Oca",
            "distrito": "San Pedro",
            "direccion_exacta": "De la iglesia católica 200m este",
        },
    )

    print("--- Estructura de Producto ---")
    print(prod_prueba)
    print("\n--- Estructura de Cliente ---")
    print(cliente_prueba)