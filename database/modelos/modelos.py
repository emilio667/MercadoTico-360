# Modelos de Estructuras de Datos para MercadoTico 360

def crear_estructura_producto(
    id_prod: str,
    nombre: str,
    precio: float,
    categoria: str,
    comercio_id: str,
    stock: int,
    atributos: dict,
) -> dict:

    return {
        "_id": id_prod,
        "nombre": nombre,
        "precio": precio,
        "categoria": categoria,
        "comercio_id": comercio_id,
        "stock": stock,
        "atributos": atributos,
    }


def crear_estructura_cliente(
    id_cliente: str,
    nombre: str,
    correo: str,
    telefono: str,
    cedula: str,
    direccion: dict,
) -> dict:

    return {
        "_id": id_cliente,
        "nombre": nombre,
        "correo": correo,
        "telefono": telefono,
        "cedula": cedula,
        "direccion": direccion,
    }


def crear_estructura_comercio(
    id_comercio: str,
    nombre: str,
    categoria: str,
    telefono: str,
    direccion: dict,
) -> dict:

    return {
        "_id": id_comercio,
        "nombre": nombre,
        "categoria": categoria,
        "telefono": telefono,
        "direccion": direccion,
    }


def crear_estructura_pedido(
    id_pedido: str,
    fecha: str,
    cliente_id: str,
    estado: str,
    lineas_detalle: list[dict],
) -> dict:

    monto_total = sum(
        item["subtotal"] for item in lineas_detalle
    )

    return {
        "_id": id_pedido,
        "fecha": fecha,
        "cliente_id": cliente_id,
        "estado": estado,
        "monto_total": monto_total,
        "lineas_detalle": lineas_detalle,
    }


if __name__ == "__main__":

    comercio_prueba = crear_estructura_comercio(
        id_comercio="COM-001",
        nombre="Tienda Central",
        categoria="Tecnologia",
        telefono="22223333",
        direccion={
            "provincia": "San José",
            "canton": "Central",
            "distrito": "Carmen",
            "direccion_exacta": "Frente al parque"
        }
    )

    print(comercio_prueba)